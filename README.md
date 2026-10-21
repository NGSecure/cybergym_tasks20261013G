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
