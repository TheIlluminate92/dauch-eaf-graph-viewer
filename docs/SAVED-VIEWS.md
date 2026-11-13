# Saved view reference

This describes `validate_view` in `graph_viewer.py` at v1.0.0. Prefer Export/Import view for routine transfer. Before manual recovery, close viewer sessions and preserve the original file as described in [operations](OPERATIONS.md#back-up-and-recover-saved-views).

The on-disk `views.json` root is a JSON list of view objects. Each object has the following fields. This is the current accepted contract, not a promised future-version migration format.

| Field | Accepted value | Default if omitted |
|---|---|---|
| name | Nonblank string, at most 100 characters before trimming | Required |
| signals | List of at most 4096 signal objects; names unique within the view | Required |
| width | Number: 0.5, 0.75, 1, 1.5, 2 or 3; booleans rejected | 1 |
| chart | lines, scatter or both | lines |
| mode | individual or overlay | individual |
| x | elapsed or clock | elapsed |
| lines | linear or hv (step) | linear |

Each signal object requires a string `name` of 1–255 characters. Optional `axis` is `left` or `right` (default left). Optional `color` is a seven-character hexadecimal color such as `#c8102e` (that value is the default). Unknown fields are not retained by validation.

A minimal on-disk example with no selected signals:

```json
[
  {
    "name": "Empty review view",
    "signals": [],
    "width": 1,
    "chart": "lines",
    "mode": "individual",
    "x": "elapsed",
    "lines": "linear"
  }
]
```

This intentionally empty view is a format example, not a useful plotted preset. Add actual available tags through the UI. A missing tag is not replaced with another signal. Settings contain neither recordings nor temporary pins or zoom ranges.

After restoring a known-good settings copy, reopen the viewer, confirm the saved name and settings, load a supported recording and verify the intended axes/signals. Stop if warnings persist; preserve the failing file for the implementation owner. A successful JSON parse alone does not prove a recovered workflow.
