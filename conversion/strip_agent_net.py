#!/usr/bin/env python3
"""Remove, within the [agent] section ONLY, the network_mode and allowed_hosts
keys plus their adjacent network-policy comment, from each task.toml passed as
an argument. The new platform injects network policy externally, so converted
bundles must not declare it; [agent] keeps only timeout_sec.

Section-scoped (never touches anything outside [agent]), marker-aware (an
unexpected [agent] comment is kept, with a stderr warning), and idempotent
(a bundle that was already stripped is a no-op). Always exits 0 so it is safe
as a `set -e` step inside convert.sh.

Usage:  python3 strip_agent_net.py <path/to/task.toml> [more task.toml ...]
"""
import sys
import re

# Phrases unique to the network-policy note (English and Chinese variants).
MARKERS = ("Public internet is cut", "公网", "allow-agent-host",
           "no-network", "/submit", "defense-in-depth")


def strip_agent_net(path):
    try:
        raw = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"  strip_agent_net: cannot read {path}: {e}", file=sys.stderr)
        return
    had_final_nl = raw.endswith("\n")
    lines = raw.split("\n")
    if had_final_nl and lines and lines[-1] == "":
        lines = lines[:-1]
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "[agent]")
    except StopIteration:
        return  # no [agent] section; nothing to do
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r'^\s*\[', lines[i]):
            end = i
            break
    body = lines[start + 1:end]
    out = []
    removed = 0
    i = 0
    n = len(body)
    while i < n:
        l = body[i]
        s = l.strip()
        if re.match(r'^\s*network_mode\s*=', l) or re.match(r'^\s*allowed_hosts\s*=', l):
            removed += 1
            i += 1
            continue
        if s.startswith("#"):
            j = i
            while j < n and body[j].strip().startswith("#"):
                j += 1
            block = body[i:j]
            if any(any(m in c for m in MARKERS) for c in block):
                removed += len(block)
                i = j
                continue
            print(f"  strip_agent_net: {path}: kept an unexpected [agent] comment "
                  f"(not the network note)", file=sys.stderr)
            out.extend(block)
            i = j
            continue
        out.append(l)
        i += 1
    if removed == 0:
        return  # already stripped / nothing matched -> idempotent no-op
    collapsed = []
    for l in out:
        if l.strip() == "" and collapsed and collapsed[-1].strip() == "":
            continue
        collapsed.append(l)
    new_lines = lines[:start + 1] + collapsed + lines[end:]
    open(path, "w", encoding="utf-8").write(
        "\n".join(new_lines) + ("\n" if had_final_nl else ""))
    print(f"  strip_agent_net: {path}: removed [agent] network policy ({removed} lines)")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        strip_agent_net(p)
