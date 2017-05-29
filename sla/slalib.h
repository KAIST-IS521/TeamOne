#pragma once
#include <openssl/rsa.h>
#include <arpa/inet.h>
#include <aio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <regex.h>
#include <time.h>
#include "gpgme.h"
#include "locale.h"
void set_aiocb(struct aiocb *cbp, int fd, void* buffer, size_t size);
int reg_check(const char* regex, void* buf);
int reg_error_number(int error);





/*To handshake fuction*/
RSA* getPubkey(const char* id);
unsigned char* gen_rand_num();
gpgme_error_t
passphrase_cb(void *opaque, const char *uid_hint, const char *passphrase_info,
              int last_was_bad, int fd);



//SLA Functions
ssize_t recvMsgUntil(int sock, const char* regex,void* buf, size_t n);
int sendMsg(int sock, const char* buf, size_t n);
int handshake(int sock, const char* ID, const char* privKeyPath, const char* passPath, const char* successMsg);
void closeSock(int sock);
int openUDPSock(char *IP, unsigned short port);
int openTCPSock(char *IP, unsigned short port);
int sendToMsg(int sock, void* buf, int len, int flags, struct sockaddr *dstaddr, int addrlen);
int recvMsgFrom(int sock, void* buf, int len, int flags, struct sockaddr *srcaddr, socklen_t *addrlen);
