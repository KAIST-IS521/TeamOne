# SLA Checker

1. `sla_checker.c`
    * SLA checker for PGP authentication
    * Use two APIs in `slalib`: `openTCPSock()` and `closeSock()`
    * Implement own APIs: `sendMsg2()`, `recvMsgUntil2()`, and `handshake2()`
    * Use `libgpgme11-dev` for GPG operations: `gpgme_op_decrypt_verify()` and `gpgme_op_encrypt()`
    * Assume that the public key of `bank` is imported in GPG (`uid`: `Happyhacking TeamOne`)

# How to Use
## Build the SLA Checkers
```
~/TeamOne$ cd sla
~/TeamOne/sla$ make
```

## How to execute `sla_checker`
```
~/TeamOne/sla$ ./build/sla_checker <ip> <port> <github_id> <private key file path> <passphrase file path>
```
