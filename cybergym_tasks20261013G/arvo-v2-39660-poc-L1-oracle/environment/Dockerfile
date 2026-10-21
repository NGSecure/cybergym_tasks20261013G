# Agent (main) container — v2, CyberGym-aligned (option A).
# The vulnerable source is handed to the agent as /workspace/repo-vul.tar.gz
# (like CyberGym's repo-vul.tar.gz), NOT pre-checked-out. We remove the image's
# own /src/freeradius-server checkout + /src/build.sh and the prebuilt sanitizer binary
# so the ONLY source of source is the tarball; the OSS-Fuzz toolchain under /src
# (compilers, llvm, fuzzing infra) is kept so the agent can build.
# Grading is unaffected: it runs on the oracle's untouched vul/fix images.
FROM n132/arvo:39660-vul

# Move off the base image's WORKDIR (/src/freeradius-server) BEFORE removing it — rm can't
# delete its own cwd, which would leave an empty /src/freeradius-server shell behind.
RUN mkdir -p /workspace
WORKDIR /workspace

RUN rm -f /bin/arvo /src/build.sh \
 && rm -rf /out/* /src/freeradius-server

# The base image's own build installed a statically linked OpenSSL 1.1.1g CLI into /usr/local/bin
# (./Configure linux-x86_64 no-shared --static ... && make install). It crashes at startup (glibc 2.31
# static link with only part of libpthread: a NULL pthread_mutex_lock), and /usr/local/bin comes first
# in PATH, so anything that runs `openssl` (update-ca-certificates, the platform's CA install) segfaults.
# Point it and c_rehash at the system's working tools; /usr/local/lib/libcrypto.a, libssl.a and the
# headers stay, so the project still builds as before.
RUN ln -sf /usr/bin/openssl /usr/local/bin/openssl \
 && if [ -x /usr/bin/c_rehash ]; then ln -sf /usr/bin/c_rehash /usr/local/bin/c_rehash; else rm -f /usr/local/bin/c_rehash; fi \
 && openssl version

# Difficulty = which of these files the agent is given (see task.toml level).
COPY repo-vul.tar.gz /workspace/repo-vul.tar.gz
COPY submit.sh /workspace/submit.sh
COPY description.txt /workspace/description.txt
RUN chmod +x /workspace/submit.sh
