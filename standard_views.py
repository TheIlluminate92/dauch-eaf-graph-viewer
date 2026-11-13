"""Focused starting points using exact tags in the supplied RPH.

These are review aids, not tuned alarm limits or decoded vendor diagnostics.
No engineering units or Smart Factor interpretation are invented from tag names.
"""
COLORS = ["#c8102e", "#2266bb", "#18835c", "#9c50ac", "#c07413", "#52616f"]


def preset(name, description, left, right=()):
    return {"name": name, "description": description, "mode": "individual", "x": "elapsed", "lines": "linear",
            "signals": [{"name": n, "axis": axis, "color": COLORS[i % len(COLORS)]}
                        for i, (n, axis) in enumerate([(n, "left") for n in left] + [(n, "right") for n in right])]}


STANDARD_VIEWS = [
    preset("1 · Power & heat progress", "Inspect total power (MWTot, left) and accumulated energy (MWH_PX3, right). Use the signal picker for program, tap and enable tags. PowerDemand uses a different recorded scale and is not assumed to be MW.",
           ["MWTot"], ["MWH_PX3"]),
    preset("2 · Phase current balance", "Compare the three phase currents with CurrentRef. Look for divergence or current dropouts; this view does not assign automatic fault thresholds.",
           ["Current1", "Current2", "Current3", "CurrentRef"]),
    preset("3 · Arc stability factors", "Compare SF1–3 on the left and VoltSF1–3 on the right. Look for changes and phase differences. Vendor factor definitions and good/bad limits require the site's tag documentation.",
           ["SF1", "SF2", "SF3"], ["VoltSF1", "VoltSF2", "VoltSF3"]),
    preset("4 · Impedance response", "Feedback ZFeedback1–3 is on the left; setpoints Sp1Imped–Sp3Imped are on the right because their recorded scales differ. Compare timing and oscillation, not numerical tracking error, until site scaling is confirmed.",
           ["ZFeedback1", "ZFeedback2", "ZFeedback3"], ["Sp1Imped", "Sp2Imped", "Sp3Imped"]),
    preset("5 · Electrode response", "Compare EPos1–3_PX3 on the left with RegOut1–3 on the right. Inspect motion and regulator-output changes. Add CIcounter1–3 when investigating recorded counter changes.",
           ["EPos1_PX3", "EPos2_PX3", "EPos3_PX3"], ["RegOut1", "RegOut2", "RegOut3"]),
]
