#!/bin/bash
# Reference solution: materialize the known-good PoC (the ARVO testcase the
# fix commit 27f9fdb1 addresses) at /workspace/poc — the 'oracle passes' side of
# the bidirectional validation. (Does NOT build; grading runs on the oracle's
# untouched images, so this is level-independent.)
set -euo pipefail

mkdir -p /workspace
base64 -d > /workspace/poc <<'B64'
OgQAAAAAAGQAQAAAAAAAAQAAAAAA/jAwFTAwACRwAAAAAAAAAF34AzJS7/7tHf8C6/7/AAIAAADoPT0AAAAODiYAAR8aAAAODg4ODi4AAAAFAAAAAADg/yxuDg4ODg4ODg4ODjoAAAAAAFsAAAAEAAAAQCRwAAAAACAAAAAAAAAAAAABAAU4AAAAAACwAD8a2D0BAAQCAAAA9SRwAAAAAAICAAAAGAECAQAE4gAAAAD7AHVpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlpaWlp2AIBAAABAP9+AAAAAHAAAAA62AIAVwQCAAAA9QICAA==
B64

echo "wrote $(wc -c < /workspace/poc) bytes to /workspace/poc"
