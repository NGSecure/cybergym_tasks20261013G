# CyberGym Task Server — ARVO sidecar
#
# Holds vul + fix binaries and ground truth PoC in an isolated container.
# Exposes an HTTP API for the agent to test PoCs (/submit) and for the
# verifier to run verification (/verify) and retrieve ground truth (/solve).
#
# The agent container never has access to these files.

FROM --platform=linux/amd64 n132/arvo:39699-fix AS fix-runner

FROM --platform=linux/amd64 n132/arvo:39699-vul

# Vul binaries (already at /out/ and /bin/arvo in the base image)
RUN mkdir -p /cybergym/vul/out /cybergym/vul/bin \
    && cp -a /out/. /cybergym/vul/out/ \
    && cp /bin/arvo /cybergym/vul/bin/arvo

# Fix binaries
RUN mkdir -p /cybergym/fix/out /cybergym/fix/bin
COPY --from=fix-runner /out/ /cybergym/fix/out/
COPY --from=fix-runner /bin/arvo /cybergym/fix/bin/arvo

# Ground truth PoC
RUN mkdir -p /tests \
    && cp /tmp/poc /tests/ground_truth_poc

# Clean up originals
RUN rm -rf /out /tmp/poc

# The base image's own build installed a statically linked OpenSSL 1.1.1g CLI into /usr/local/bin
# (./Configure linux-x86_64 no-shared --static ... && make install). It crashes at startup (glibc 2.31
# static link with only part of libpthread: a NULL pthread_mutex_lock), and /usr/local/bin comes first
# in PATH, so anything that runs `openssl` (update-ca-certificates, the platform's CA install) segfaults.
# Point it and c_rehash at the system's working tools; /usr/local/lib/libcrypto.a, libssl.a and the
# headers stay, so the project still builds as before.
RUN ln -sf /usr/bin/openssl /usr/local/bin/openssl \
 && if [ -x /usr/bin/c_rehash ]; then ln -sf /usr/bin/c_rehash /usr/local/bin/c_rehash; else rm -f /usr/local/bin/c_rehash; fi \
 && openssl version

COPY task_server.py /task_server.py

EXPOSE 9111
CMD ["python3", "-u", "/task_server.py"]
