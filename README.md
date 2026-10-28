# cybergym_tasks20261013G

95 个 ARVO prime bundle 转换成新平台（CyberGym）格式的结果，在 `cybergym_tasks20261013G/`；转换方法见 `conversion/SKILL.md`。

## 已知问题和修改

- **2026-10-21：freeradius-server 的 5 个 bundle 改为 v0.0.2 镜像。** `arvo-v2-39657`、`39660`、`39699`、`39986`、`40118`
  在平台上启动时报 `Failed to install OpenSandbox ca_cert into the sandbox trust store: Segmentation fault (core dumped)`。
  原因在 ARVO 原始镜像：镜像构建时用 `./Configure linux-x86_64 no-shared --static ... && make install` 编译 OpenSSL 1.1.1g，
  顺带把一个静态链接的 `openssl` 命令行工具装进了 `/usr/local/bin`；它一启动就段错误（glibc 2.31 静态链接只链进了一部分 libpthread），
  而 `/usr/local/bin` 在 PATH 里排在 `/usr/bin` 前面，平台安装 CA 证书时调用的 `update-ca-certificates`（`openssl rehash`）就会崩溃。
  修改：这 5 个 bundle 的 agent 镜像和 task-server 镜像都把 `/usr/local/bin/openssl`、`c_rehash` 指向系统的 `/usr/bin/openssl`、
  `/usr/bin/c_rehash`，构建时检查 `openssl version`；`/usr/local/lib` 里的 `libcrypto.a`、`libssl.a` 和头文件保留，判定用的漏洞版、
  安全版程序没有变化。本地重建后检查过：两个镜像里 `openssl version` 正常（OpenSSL 1.1.1f），`update-ca-certificates` 能装入测试 CA；
  标准答案 PoC 仍判为通过（漏洞版退出码 1，安全版 0），空 PoC 仍判为不通过。镜像标签改为 `v0.0.2`：请对这 5 个重新运行 `build.sh`
  和 `push.sh`。其余 90 个 bundle 没有改动。

- **2026-10-28：agent 镜像不再带参考答案 `/tmp/poc` 和源码的版本历史；全部 95 个 bundle 的镜像标签改为 `v0.0.2`（freeradius 的 5 个从 `v0.0.2` 改为 `v0.0.3`）。**
  ARVO 原始镜像 `n132/arvo:<id>-vul` 在 `/tmp/poc` 存着这个漏洞的复现输入，和 `solution/solve.sh` 写出的标准答案逐字节相同，
  所有用户可读，平台上已有 agent 直接提交它拿到 reward=1。另外，删掉项目目录以后，`/src` 下还留着依赖库（zlib、libjpeg-turbo 等）
  或项目另一份副本（如 capstonemaster）的 git/hg 仓库；它们是 2024 年克隆的，历史一直延续到漏洞修复之后，agent 能从中翻到上游的修复提交。
  修改：`environment/Dockerfile` 在删除 `/bin/arvo`、`/src/build.sh`、`/out/*` 和项目目录那一步之后，增加 `RUN rm -f /tmp/poc` 和
  `RUN find /src \( -name .git -o -name .hg \) -prune -exec rm -rf {} +`（只删版本库元数据，源码保留，agent 照样能编译）。
  改动由 `conversion/harden_agent_dockerfile.py` 完成，以后 `convert.sh` 转换新 bundle 时也会做这一步。task-server 镜像从自己那份基础镜像构建，
  标准答案仍在它的 `/tests/ground_truth_poc`，判定不受影响。本地用 Docker 实测了 arvo-v2-783、8867、39699：新镜像里没有 `/tmp/poc`，
  `/src` 下没有 `.git`、`.hg`（旧镜像的 `/tmp/poc` 与标准答案逐字节相同；8867 旧镜像的 `/src/capstonemaster` 里能看到 2,930 个比漏洞版本新的提交）；
  783 的完整评测结果与修改前一致（标准答案 reward=1，空 PoC reward=0），在新镜像里从 `repo-vul.tar.gz` 编译 pcre2 和 fuzzer、复现崩溃都正常；freeradius 的 bundle 构建时的 `openssl version` 检查照常通过。
  请对本仓库的 bundle 重新运行 `build.sh` 和 `push.sh`（两个镜像都用新标签）。
