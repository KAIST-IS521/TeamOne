/*
 * SLA chacker: PGP authentication
 */
#include <arpa/inet.h>
#include <aio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <regex.h>
#include "slalib.h"

#define MAX_LEN 1024

/* hexdump() from https://gist.github.com/ccbrown/9722406 */
void hexdump(const void* data, size_t size) {
    char ascii[17];
    size_t i, j;
    ascii[16] = '\0';
    for (i = 0; i < size; ++i) {
        printf("%02X ", ((unsigned char*)data)[i]);
        if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
            ascii[i % 16] = ((unsigned char*)data)[i];
        } else {
            ascii[i % 16] = '.';
        }
        if ((i+1) % 8 == 0 || i+1 == size) {
            printf(" ");
            if ((i+1) % 16 == 0) {
                printf("|  %s \n", ascii);
            } else if (i+1 == size) {
                ascii[(i+1) % 16] = '\0';
                if ((i+1) % 16 <= 8) {
                    printf(" ");
                }
                for (j = (i+1) % 16; j < 16; ++j) {
                    printf("   ");
                }
                printf("|  %s \n", ascii);
           }
        }
     }
}

int recvMsgUntilBK(int cli_fd) {
    int len = 0, i = 0;
    char buf[MAX_LEN] = {0};
    int is_received = 0;

    while((len = read(cli_fd, buf, sizeof(buf)-1)) > 0){
        buf[len] = 0;
#ifdef	DEBUG
        setbuf(stdout, NULL);
        if(fputs(buf, stdout) == EOF){
           printf("\n Error: fputs error\n");
        }
#endif
        for(i=0;i<len;i++){
          if(buf[i] == '>') {
              is_received = 1;
              break;
          } // if '>' go next
        }

        if(is_received == 1) break;
    }
    if ( len <= 0 ) return -1;

    return 0;
}

int sendMsg(int cli_fd, char* buf) {
    if ( buf == NULL ) return -1;
    int len = strlen(buf);
    return write(cli_fd, buf, len);
}

int main(int argc, char *argv[]) {
    int cli_fd = 0;

    if (argc != 3){
        printf("Usage: %s <ip> <port>\n", argv[0]);
        exit(1); 
    }

    /* read ip and port */
    char *ip = argv[1];
    int port = atoi(argv[2]);

    /* connect to the server */
    cli_fd = openTCPSock(ip, port);

    if(cli_fd <0){
        printf("Failed to open socket (rv=%d) return 2\n", cli_fd);
        exit(2);		// SLA return 2 : cannot connect
    }

    /* get the initial msg from the server */
    // FIXME - replace with recvMsgUntil()
    printf("1. Receiving the initial msg from the server...\n");
    recvMsgUntilBK(cli_fd);

    /* send the menu for registration */
    // FIXME - replace with sendMsg()
    printf("2. Sending the selection to the server(login)...\n");
    if ( sendMsg(cli_fd, "1\n") == -1 ) exit(1);	// 1. login

    /* get the msg from the server */
    // FIXME - replace with recvMsgUntil()
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);

    if ( sendMsg(cli_fd, "user1\n") == -1 ) exit(1);
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "pass1\n") == -1 ) exit(1);
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);

    printf("3. Transfer function check\n");
    if ( sendMsg(cli_fd, "3\n") == -1 ) exit(1); // Transfer
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "admin\n") == -1 ) exit(1);	// Receiver's id
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "0\n") == -1 ) exit(1); // Transfer
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "test\n") == -1 ) exit(1); // Transfer
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "y\n") == -1 ) exit(1); // Transfer
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "\n") == -1 ) exit(1); // Back to main menu
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
   
    printf("4. Transaction history function check\n");
    if ( sendMsg(cli_fd, "2\n") == -1 ) exit(1); // Transaction history
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "\n") == -1 ) exit(1); // Back to main menu
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);

    printf("5. Balance check function check\n");
    if ( sendMsg(cli_fd, "1\n") == -1 ) exit(1); // Balance
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "\n") == -1 ) exit(1); // Back to main menu
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);

    printf("6. Logout function check\n");
    if ( sendMsg(cli_fd, "5\n") == -1 ) exit(1); // Logout
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);
    if ( sendMsg(cli_fd, "3\n") == -1 ) exit(1); // Terminate
    if ( recvMsgUntilBK(cli_fd) == -1 ) exit(1);

    closeSock(cli_fd);
    printf("Done. return 0\n");

    return 0;		// SLA check 0 : normal
}
