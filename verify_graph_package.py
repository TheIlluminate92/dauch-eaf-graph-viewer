"""Exercise the packaged executable, not the source interpreter.

Five modified copies of the one supplied RPH exercise multi-file comparison.
They are test fixtures only, never represented as additional production heats.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import math
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from rph_reader import read_rph

EXE = Path(sys.argv[1]).resolve()
REAL = Path(os.environ.get("EAF_RPH_DIR", Path.home() / "Downloads")) / "Hoeganaes23217.rph"


def call(url, route, body=None, raw=False):
    req=Request(url+route,data=body if raw else json.dumps(body).encode() if body is not None else None)
    with urlopen(req,timeout=60) as r:return json.load(r)


def launch(directory):
    p=subprocess.Popen([str(EXE),'--no-browser','--views',directory],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    url=p.stdout.readline().strip()
    if not url.startswith('http://127.0.0.1:'):
        p.terminate();raise AssertionError('Packaged viewer failed to start: '+p.stderr.read())
    return p,url


def main():
    if not REAL.is_file():
        raise SystemExit("Private fixture Hoeganaes23217.rph is required; set EAF_RPH_DIR to its folder.")
    with tempfile.TemporaryDirectory() as d:
        p,url=launch(d)
        try:
            raw=REAL.read_bytes()
            real=call(url,'upload?name=Hoeganaes23217.rph',raw,True)
            # Change just the first recorded value to distinguish comparison inputs.
            offset=23
            for _ in range(struct.unpack_from('<H',raw,21)[0]):offset+=1+raw[offset]
            offset+=6
            for i in range(1,6):
                changed=bytearray(raw);struct.pack_into('<f',changed,offset,9000+i)
                call(url,f'upload?name=SYNTHETIC-comparison-{i}.rph',bytes(changed),True)
            state=call(url,'state');assert len(state['files'])==6
            assert all(f['rows']==3701 and len(f['signals'])==644 for f in state['files'])
            for preset in state['presets']:
                for f in state['files']:
                    plotted=call(url,'plot',{**preset,'files':[f['id']]})
                    assert not plotted['missing'];assert len(plotted['traces'])==len(preset['signals'])
                    assert all(t['line']['width']==1 for t in plotted['traces'])
                stacked=call(url,'plot',{**preset,'files':[f['id'] for f in state['files']]})
                assert len(stacked['traces'])==6*len(preset['signals'])
                assert all(len(t['x'])==3716 for t in stacked['traces'])
            # Fetch every signal, individually, to check the complete column map.
            for name in real['signals']:
                plotted=call(url,'plot',{'files':[real['id']],'signals':[{'name':name}]})
                assert len(plotted['traces'])==1 and not plotted['missing']
            recording=read_rph(raw)
            # Every real tag must also work as X; it must contain raw signal values,
            # not elapsed time or values drawn from another file.
            for column,name in enumerate(real['signals']):
                xy=call(url,'plot',{'files':[real['id']],'x':'signal','x_signal':name,'chart':'scatter','signals':[{'name':'Current1','axis':'right'}]})
                trace=xy['traces'][0];expected=float(recording.values[0,column])
                assert trace['x'][0]==(expected if math.isfinite(expected) else None)
                assert len(trace['x'])==len(trace['y'])==len(trace['customdata'])==3716
                assert trace['yaxis']=='y2' and trace['mode']=='markers'
            for chart in ('lines','scatter','both'):
                xy=call(url,'plot',{'files':[f['id'] for f in state['files']],'x':'signal','x_signal':'MWTot','chart':chart,'signals':[{'name':'Current1'}]})
                assert len(xy['traces'])==6 and not xy['missing']
                assert all(not t['connectgaps'] for t in xy['traces'])
            saved={**state['presets'][3],'name':'Package test · Sergio','mode':'overlay','width':0.5,'chart':'scatter'}
            for chart,mode in [('lines','lines'),('scatter','markers'),('both','lines+markers')]:
                plotted=call(url,'plot',{**saved,'chart':chart,'files':[f['id'] for f in state['files']]})
                assert all(t['mode']==mode for t in plotted['traces'])
                assert plotted['traces'][0]['marker']['symbol']!=plotted['traces'][len(saved['signals'])]['marker']['symbol']
            for width in (0.5,0.75,1,1.5,2,3):
                plotted=call(url,'plot',{**saved,'width':width,'files':[f['id'] for f in state['files']]})
                assert all(t['line']['width']==width for t in plotted['traces'])
            call(url,'save',saved)
            xy_saved={**saved,'name':'Saved X-Y','x':'signal','x_signal':'MWTot','signals':[{'name':'Current1'}]}
            call(url,'save',xy_saved)
            try:call(url,'upload?name=broken.rph',raw[:-10],True);raise AssertionError('Truncated file accepted')
            except HTTPError as e:assert e.code==400
            with urlopen(url+'plotly.js') as r:assert len(r.read())>1000000
            with urlopen(url) as r:assert b'Previous' in r.read()
            with urlopen(url+'cursor_tools.js') as r:assert b'PinStore' in r.read()
        finally:p.terminate();p.wait(timeout=10)
        p,url=launch(d)
        try:
            state=call(url,'state');assert state['views'][0]['name']==saved['name'];assert state['views'][0]['mode']=='overlay'
            assert state['views'][0]['width']==0.5
            assert state['views'][0]['chart']=='scatter'
            xy_view=next(v for v in state['views'] if v['name']=='Saved X-Y')
            assert xy_view['x']=='signal' and xy_view['x_signal']=='MWTot'
        finally:p.terminate();p.wait(timeout=10)
    print('PASS: packaged engine; real RPH + five synthetic variants; 30 individual preset plots; 5 overlays; all 644 signals on Y AND X; six-file X-Y in all styles; time and X-Y saved-view restart; malformed-file rejection; bundled offline assets.')


if __name__=='__main__':main()
