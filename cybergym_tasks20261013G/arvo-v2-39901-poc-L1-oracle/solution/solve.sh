#!/bin/bash
# Reference solution: materialize the known-good PoC (the ARVO testcase the
# fix commit 30ebadfe addresses) at /workspace/poc — the 'oracle passes' side of
# the bidirectional validation. (Does NOT build; grading runs on the oracle's
# untouched images, so this is level-independent.)
set -euo pipefail

mkdir -p /workspace
base64 -d > /workspace/poc <<'B64'
s3J4Kw4rKysrKysrKysrKysraCsrKysrKysrKysYKysrK2graysrKysrKysrKysrKysrKyuzcm0rLCsrKysrKysrKysrK3VzZXJTZXRBdXRoS2V5ACArKysrK2grKysrKysrKysrKysrKysrKyspDSsrKysrKysrKytoKysrKysrKysrKysrKytzK2srKysrKysrKysrKysrK56JeCsOKysrKwAAAABoKysrAAH/7GgrKysrKysrKysAAACAMSsrKysrKysrKysAKysrK56JeCsOKysrKwAAAABoKwAAAGgrKysAAf/saCsrKysrKysrKwAAACtoKzArs3J4Kw4rKysrKzMrKysrKysraCsrKysrKysrKysrKysrK2graysrKysrKysrKysrKysAASuzcm0rLCsdKysrK2gpKysrKyv/////KysrKysrKyspDSsrK3grDisrKysrMysrKysrKytoKysrKysrKysrKysrKysrKysrKysraCsrKysrKysrKysrKysrcytrKys=
B64

echo "wrote $(wc -c < /workspace/poc) bytes to /workspace/poc"
