"""Local-only graph viewer service. The Windows launcher owns its lifetime.

The browser supplies file bytes; the service keeps readings in memory and saves
only named view settings to disk. A random URL protects each local session.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import sys
import threading
from urllib.parse import urlparse, parse_qs
import webbrowser

import numpy as np
from plotly.offline import get_plotlyjs
from rph_reader import read_rph
from standard_views import STANDARD_VIEWS

MAX_FILE = 128 * 1024 * 1024
MAX_SESSION = 512 * 1024 * 1024


@contextmanager
def views_lock(folder):
    """Coordinate saves from two viewer windows; OS releases the lock on exit."""
    with (folder / "views.lock").open("a+b") as handle:
        handle.seek(0, 2)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def validate_view(view):
    if not isinstance(view, dict) or not isinstance(view.get("name"), str) or not view["name"].strip():
        raise ValueError("Give the view a name.")
    if len(view["name"]) > 100:
        raise ValueError("View names may contain at most 100 characters.")
    signals = view.get("signals")
    if not isinstance(signals, list) or len(signals) > 4096:
        raise ValueError("Invalid signal selection.")
    clean, seen = [], set()
    for s in signals:
        if not isinstance(s, dict) or not isinstance(s.get("name"), str) or not 1 <= len(s["name"]) <= 255:
            raise ValueError("Invalid signal name.")
        color = s.get("color", "#c8102e")
        if not isinstance(color, str) or len(color) != 7 or color[0] != "#" or any(c not in "0123456789abcdefABCDEF" for c in color[1:]):
            raise ValueError("Invalid signal color.")
        if s["name"] in seen:
            raise ValueError("A signal was selected twice.")
        seen.add(s["name"])
        if s.get("axis", "left") not in ("left", "right"):
            raise ValueError("Signal axis must be left or right.")
        clean.append({"name": s["name"], "axis": "right" if s.get("axis") == "right" else "left", "color": color})
    # Older saved views have no width setting and inherit the finer default.
    width = view.get("width", 1)
    if isinstance(width, bool) or not isinstance(width, (int, float)) or width not in (0.5, 0.75, 1, 1.5, 2, 3):
        raise ValueError("Choose a line thickness between 0.5 and 3 pixels.")
    chart = view.get("chart", "lines")
    if chart not in ("lines", "scatter", "both"):
        raise ValueError("Choose Lines, Scatter, or Lines + points.")
    for field, default, choices in (("mode", "individual", ("individual", "overlay")),
                                     ("x", "elapsed", ("elapsed", "clock", "signal")),
                                     ("lines", "linear", ("linear", "hv"))):
        if view.get(field, default) not in choices:
            raise ValueError(f"Invalid {field} setting.")
    x_mode = view.get("x", "elapsed")
    x_signal = view.get("x_signal", "") if x_mode == "signal" else ""
    if x_mode == "signal" and (not isinstance(x_signal, str) or not 1 <= len(x_signal) <= 255 or not x_signal.strip()):
        raise ValueError("Choose a recorded signal for the X axis.")
    return {"name": view["name"].strip(), "signals": clean, "width": width, "chart": chart,
            "mode": "overlay" if view.get("mode") == "overlay" else "individual",
            "x": x_mode, "x_signal": x_signal,
            "lines": "hv" if view.get("lines") == "hv" else "linear"}


class Session:
    def __init__(self, views):
        self.path = Path(views)
        self.path.mkdir(parents=True, exist_ok=True)
        self.files = {}
        self.next_style = 0
        self.views = {}
        self.lock = threading.RLock()
        self.warning = ""
        self.reload_views()

    def read_views(self):
        saved = self.path / "views.json"
        if not saved.exists():
            return {}
        values = json.loads(saved.read_text(encoding="utf-8"))
        if not isinstance(values, list):
            raise ValueError("Saved views must be a list.")
        clean = [validate_view(v) for v in values]
        return {v["name"]: v for v in clean}

    def reload_views(self):
        with self.lock, views_lock(self.path):
            try:
                self.views = self.read_views()
                self.warning = ""
            except (ValueError, TypeError, OSError):
                # Never silently overwrite damaged settings when starting up.
                self.warning = "Saved views could not be read. Original settings retained; fix or move views.json before saving."

    def add(self, name, raw):
        if not name.lower().endswith(".rph"):
            raise ValueError("Choose an RPH file.")
        key = hashlib.sha256(raw).hexdigest()[:24]
        with self.lock:
            if key in self.files:
                return self.metadata(key)
            if sum(f["bytes"] for f in self.files.values()) + len(raw) > MAX_SESSION:
                raise ValueError("Session is full (512 MB). Remove a recording before adding another.")
            rec = read_rph(raw)
            self.files[key] = {"name": name.replace("\\", "/").split("/")[-1], "recording": rec, "bytes": len(raw), "style": self.next_style}
            self.next_style += 1
            return self.metadata(key)

    def metadata(self, key):
        f = self.files[key]
        r = f["recording"]
        return {"id": key, "name": f["name"], "signals": r.names,
                "rows": len(r.seconds), "minutes": (r.seconds[-1] - r.seconds[0]) / 60,
                "start": datetime.fromtimestamp(r.seconds[0], timezone.utc).isoformat(),
                "gaps": r.gaps, "nonfinite": int(np.sum(~np.isfinite(r.values)))}

    def save(self, view):
        view = validate_view(view)
        with self.lock, views_lock(self.path):
            if self.warning:
                raise ValueError(self.warning)
            # Re-read under the shared lock so another window's saves survive.
            updated = self.read_views()
            updated[view["name"]] = view
            temp = self.path / ("views-" + secrets.token_hex(8) + ".tmp")
            try:
                temp.write_text(json.dumps(list(updated.values()), indent=2), encoding="utf-8")
                os.replace(temp, self.path / "views.json")
            finally:
                temp.unlink(missing_ok=True)
            self.views = updated
        return view

    def data(self, request):
        traces, missing = [], []
        if not isinstance(request, dict):
            raise ValueError("Plot settings must be an object.")
        view = validate_view({**request, "name": "Current"})
        ids = request.get("files", [])
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            raise ValueError("Invalid recording selection.")
        # Return every sample; a missing-data marker breaks lines across gaps.
        with self.lock:
            points = sum(len(self.files[k]["recording"].seconds) for k in set(ids) if k in self.files) * len(view["signals"])
            if points > 5_000_000:
                raise ValueError("This comparison exceeds 5 million plotted samples. Select fewer signals or recordings; raw data has not been reduced.")
            for idx, key in enumerate(dict.fromkeys(ids)):
                if key not in self.files:
                    raise ValueError("A recording was removed. Refresh the file list.")
                f = self.files[key]
                idx = f["style"]
                r = f["recording"]
                gaps = np.flatnonzero(np.diff(r.seconds) > 5) + 1
                if view["x"] == "signal":
                    if view["x_signal"] not in r.names:
                        missing.append(f'{f["name"]}: X signal {view["x_signal"]}')
                        continue
                    # Pair X and Y from the same row in the same recording.
                    # Never sort X, interpolate, or join samples across heats.
                    base_x = r.values[:, r.names.index(view["x_signal"])].astype(float)
                else:
                    base_x = (r.seconds-r.seconds[0])/60 if view["x"] == "elapsed" else r.seconds*1000
                x = np.insert(base_x, gaps, np.nan)
                x = [float(v) if np.isfinite(v) else None for v in x]
                sample_info = None
                if view["x"] == "signal":
                    stamps = np.insert(r.seconds, gaps, np.nan)
                    sample_info = [[datetime.fromtimestamp(t, timezone.utc).isoformat(timespec="milliseconds"), float((t-r.seconds[0])/60)] if np.isfinite(t) else None for t in stamps]
                for s in view["signals"]:
                    if s["name"] not in r.names:
                        missing.append(f'{f["name"]}: {s["name"]}')
                        continue
                    y = np.insert(r.values[:, r.names.index(s["name"])].astype(float), gaps, np.nan)
                    # Plotly uses trace IDs in CSS selectors when traces change.
                    # Tags contain spaces, slashes and punctuation: hash them and
                    # start with a letter so every ID is a valid CSS identifier.
                    trace_id = "t" + hashlib.sha256((key + "\0" + s["name"]).encode()).hexdigest()[:24]
                    trace = {"type": "scatter", "uid": trace_id, "mode": {"lines": "lines", "scatter": "markers", "both": "lines+markers"}[view["chart"]], "name": f'{f["name"]} · {s["name"]}',
                        "x": x, "y": [float(v) if np.isfinite(v) and x[i] is not None else None for i, v in enumerate(y)],
                        "yaxis": "y2" if s["axis"] == "right" else "y", "connectgaps": False,
                        "line": {"color": s["color"], "width": view["width"], "shape": view["lines"], "dash": ["solid", "dash", "dot", "dashdot", "longdash", "longdashdot"][idx % 6]},
                        "marker": {"color": s["color"], "size": 3, "opacity": 0.7,
                                   "symbol": ["circle", "square", "diamond", "triangle-up", "cross", "x"][idx % 6]},
                        "hovertemplate": "%{x}<br>%{y:.5g}<extra>%{fullData.name}</extra>"}
                    if sample_info is not None:
                        trace["customdata"] = sample_info
                        trace["hovertemplate"] = "X: %{x:.7g}<br>Y: %{y:.7g}<br>Recorded time: %{customdata[0]}<br>Elapsed: %{customdata[1]:.5g} min<extra>%{fullData.name}</extra>"
                    traces.append(trace)
        return {"traces": traces, "missing": missing}


def make_server(session, port=0):
    token = secrets.token_urlsafe(32)
    prefix = "/" + token + "/"
    assets = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, payload, status=200, kind="application/json"):
            body = json.dumps(payload, allow_nan=False).encode() if kind == "application/json" else payload
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def handle_request(self):
            url = urlparse(self.path)
            expected_host = f"127.0.0.1:{self.server.server_port}"
            if self.headers.get("Host") != expected_host or not url.path.startswith(prefix):
                self.send({"error": "Invalid session."}, 403)
                return
            origin = self.headers.get("Origin")
            if origin and origin != "http://" + expected_host:
                self.send({"error": "Invalid origin."}, 403)
                return
            route = url.path[len(prefix):]
            try:
                if self.command == "GET":
                    if route == "":
                        self.send((assets / "viewer.html").read_bytes(), kind="text/html")
                    elif route == "cursor_tools.js":
                        self.send((assets / "cursor_tools.js").read_bytes(), kind="application/javascript")
                    elif route == "plotly.js":
                        self.send(get_plotlyjs().encode(), kind="application/javascript")
                    elif route == "state":
                        session.reload_views()
                        with session.lock:
                            self.send({"files": [session.metadata(k) for k in session.files], "views": list(session.views.values()), "presets": STANDARD_VIEWS, "warning": session.warning})
                    else:
                        self.send({"error": "Not found"}, 404)
                    return
                size = int(self.headers.get("Content-Length", "0"))
                limit = MAX_FILE if route == "upload" else 2 * 1024 * 1024
                if not 0 < size <= limit:
                    raise ValueError("Request is empty or too large (RPH limit: 128 MB).")
                raw = self.rfile.read(size)
                if len(raw) != size:
                    raise ValueError("Incomplete upload.")
                if route == "upload":
                    self.send(session.add(parse_qs(url.query).get("name", [""])[0], raw))
                    return
                data = json.loads(raw)
                if route == "plot":
                    self.send(session.data(data))
                elif route == "save":
                    self.send(session.save(data))
                elif route == "remove":
                    with session.lock:
                        session.files.pop(data["id"], None)
                    self.send({"ok": True})
                else:
                    self.send({"error": "Not found"}, 404)
            except (ValueError, KeyError, TypeError, OSError) as exc:
                self.send({"error": str(exc)}, 400)

        do_GET = handle_request
        do_POST = handle_request

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    return server, f"http://127.0.0.1:{server.server_port}{prefix}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("--views", default=str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Dauch" / "EAF Graph Viewer"))
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    session = Session(args.views)
    for path in args.files:
        p = Path(path)
        if p.stat().st_size > MAX_FILE:
            raise ValueError("RPH exceeds 128 MB.")
        session.add(p.name, p.read_bytes())
    server, url = make_server(session)
    print(url, flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    server.serve_forever()


if __name__ == "__main__":
    main()
