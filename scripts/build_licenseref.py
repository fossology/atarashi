"""Extend the license list with ScanCode's LicenseRef-scancode-* namespace.

Off by default: this changes which identifiers the agent emits, which is a product
decision for the maintainers rather than a build detail. Run it, point the agent at
the output, and the extra licenses become nameable.

`LicenseRef-<idstring>` is the SPDX spec's own mechanism for licenses not on the
SPDX List, and FOSSology already emits that prefix so its SPDX documents validate.
ScanCode publishes exactly that form, so ingesting LicenseDB's non-SPDX half is
standards-compliant rather than a namespace fork.

Reads the locally installed licensedcode data — no network — and writes an extended
copy of processedLicenses.csv.

**Measured, so the trade is not a guess.** 774 -> 2,474 licenses adds 953 indexed
units and costs nothing measurable: match latency 31.7 -> 32.0 ms/query, and DEP-5
in-sample moves precision 0.8789 -> 0.8752, R@1 0.8435 -> 0.8465, exact-set
0.868 -> 0.858 — flat within noise.

**But nameable is not detectable.** On the Software Heritage annotated sample it
takes licenses the agent can name from 66/81 to 77/81, and identifies none of the
eleven it gained: only 262 of the 1,700 added licenses carry any short-form rule
(median 1), so they are matchable against a full body alone — the configuration the
eval findings measure at R@1 ~0.004 on real headers. The learned ranker also declines
on them, since `family()` returns OTHER for a LicenseRef id and the gate refuses
outside trained families. Worth having so an auditor sees the right name in the
verbatim regime; not a fix for tail identification.

    python scripts/build_licenseref.py /tmp/licenses_extended.csv
"""
import sys
import pandas as pd
from licensedcode.models import load_licenses, licenses_data_dir

# Non-identifying buckets: ScanCode's way of saying "there is licensing here but I
# cannot name it". Indexing them would turn an abstention into a confident wrong
# answer, and the eval's own SKIP_KEYS drops them from ground truth too.
SKIP = {"unknown-license-reference", "unknown", "proprietary-license",
        "warranty-disclaimer", "generic-cla", "other-permissive", "other-copyleft",
        "commercial-license", "public-domain", "public-domain-disclaimer",
        "free-unknown", "generic-exception", "generic-export-compliance"}

ROOT = "/Users/swapnil.dutta/Projects/oss/fossology-gsoc"
base = pd.read_csv(f"{ROOT}/atarashi/atarashi/data/licenses/processedLicenses.csv")
have = {str(s).lower() for s in base["shortname"]}

lic = load_licenses(licenses_data_dir, with_deprecated=False)
rows, skipped = [], 0
for key, entry in lic.items():
    spdx = (entry.spdx_license_key or "").strip()
    if not spdx or not spdx.lower().startswith("licenseref-"):
        continue                      # already an SPDX id: base list has it
    if key in SKIP:
        skipped += 1
        continue
    text = (entry.text or "").strip()
    if len(text.split()) < 15:        # nothing matchable
        continue
    if spdx.lower() in have:
        continue
    rows.append({"shortname": spdx, "fullname": entry.short_name or spdx,
                 "text": text, "license_header": "", "url": entry.homepage_url or "",
                 "deprecated": False})

ext = pd.concat([base, pd.DataFrame(rows)], ignore_index=True)
for col in base.columns:
    if col not in ext.columns:
        ext[col] = ""
ext = ext[base.columns]
out = sys.argv[1]
ext.to_csv(out, index=False)
print(f"base {len(base)} + {len(rows)} LicenseRef-scancode entries "
      f"({skipped} non-identifying skipped) = {len(ext)} -> {out}")
