# SLA Checker

1. `sla_checker.c`
    * SLA checker for PGP authentication
    * Use two APIs in `slalib`: `openTCPSock()` and `closeSock()`
    * Implement own APIs: `sendMsg2()`, `recvMsgUntil2()`, and `handshake2()`
    * Assume that the public key of `bank` is imported in GPG \
      (`uid`: `Happyhacking TeamOne`)

# How to Use
## Build the SLA Checkers
```
~/TeamOne$ cd sla
~/TeamOne/sla$ make
```

## How to execute `sla_checker`
```
~/TeamOne/sla$ ./build/sla_checker <ip> <port> <github_id>
```

- `ip`: IP address of the bank server
- `port`: Port number of the bank server (`1588`)
- `github_id`: Github ID that has the paired private key in `./client.key` and the passphrase stored in `./passwd`
