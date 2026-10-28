#!/usr/bin/env python3
"""Keep the reference answer and the upstream fix out of the agent (main) image.

The ARVO base image n132/arvo:<id>-vul keeps ARVO's reproducer for the bug at /tmp/poc
(the same file solution/solve.sh writes), and the checkouts it leaves under /src
(dependencies, fuzzing tools, another copy of the project) keep their full git/hg
history, which runs past the vulnerable commit to the upstream fix. Right after the
Dockerfile's `RUN rm -f /bin/arvo /src/build.sh && rm -rf /out/* /src/<project>` step,
this inserts

    RUN rm -f /tmp/poc
    RUN find /src \\( -name .git -o -name .hg \\) -prune -exec rm -rf {} +

The task-server image is built from its own copy of the base image (its Dockerfile
copies /tmp/poc to /tests/ground_truth_poc), so grading does not change.

Idempotent: a Dockerfile that already has `RUN rm -f /tmp/poc` is left as it is.

    python3 conversion/harden_agent_dockerfile.py <bundle>/environment/Dockerfile...

Prints HARDENED or UNCHANGED per file; exits 1 if a file has no such rm step.
"""
import re
import sys

BLOCK = r"""
# The base image keeps ARVO's reproducer for this bug at /tmp/poc, the same file
# solution/solve.sh writes: the reference answer. The agent must not see it (the
# task-server is built from its own copy of the base image, so grading is unaffected).
RUN rm -f /tmp/poc

# The checkouts left under /src (dependencies, fuzzing tools, another copy of the
# project) keep their full git/hg history, which runs past the vulnerable commit to the
# upstream fix. Drop the version-control metadata; the source trees stay for building.
RUN find /src \( -name .git -o -name .hg \) -prune -exec rm -rf {} +
"""

RM_STEP = re.compile(r"^RUN rm -f /bin/arvo /src/build\.sh \\\n && rm -rf /out/\* \S+\n", re.M)


def main(paths):
    bad = 0
    for p in paths:
        with open(p, newline="") as f:
            s = f.read()
        if re.search(r"^RUN rm -f /tmp/poc$", s, re.M):
            print("UNCHANGED  %s" % p)
            continue
        m = RM_STEP.search(s)
        if not m:
            print("NO RM STEP %s" % p, file=sys.stderr)
            bad += 1
            continue
        with open(p, "w", newline="") as f:
            f.write(s[:m.end()] + BLOCK + s[m.end():])
        print("HARDENED   %s" % p)
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
