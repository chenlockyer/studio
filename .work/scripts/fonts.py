# -*- coding: utf-8 -*-
"""TASK 3: subset fonts -> assets/fonts/*.woff2"""
import os, subprocess, sys, json

ROOT = r"D:\code\unitree-site"
W = os.path.join(ROOT, ".work")
FDIR = os.path.join(W, "fonts")
OUT = os.path.join(ROOT, "assets", "fonts")
PY = sys.executable

NOTO_TXT = os.path.join(W, "noto-glyphs.txt")
EPI_TXT = os.path.join(W, "epilogue-glyphs.txt")

JOBS = [
    # (source ttf, text file, output, extra args)
    ("NotoSansSC-400.ttf", NOTO_TXT, "noto-sans-sc-400.subset.woff2",
     ["--flavor=woff2", "--layout-features=*", "--no-hinting", "--desubroutinize"]),
    ("NotoSansSC-500.ttf", NOTO_TXT, "noto-sans-sc-500.subset.woff2",
     ["--flavor=woff2", "--layout-features=*", "--no-hinting", "--desubroutinize"]),
    ("NotoSansSC-700.ttf", NOTO_TXT, "noto-sans-sc-700.subset.woff2",
     ["--flavor=woff2", "--layout-features=*", "--no-hinting", "--desubroutinize"]),
    ("Epilogue-VF.ttf", EPI_TXT, "epilogue-latin.woff2",
     ["--flavor=woff2", "--layout-features=*", "--no-hinting"]),
]

rows = []
for src, txt, outname, extra in JOBS:
    outp = os.path.join(OUT, outname)
    cmd = [PY, "-m", "fontTools.subset", os.path.join(FDIR, src),
           "--text-file=%s" % txt, "--output-file=%s" % outp] + extra
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED", outname)
        print(r.stdout[-3000:]); print(r.stderr[-3000:])
        sys.exit(1)
    b = os.path.getsize(outp)
    rows.append({"file": outname, "bytes": b, "source": src})
    print("%-34s %7d B (%.1f KB)" % (outname, b, b / 1024))

json.dump(rows, open(os.path.join(W, "font-results.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
tot = sum(r["bytes"] for r in rows)
print("\nfonts total=%d B (%.1f KB)" % (tot, tot / 1024))
