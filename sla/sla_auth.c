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

int main(int argc, char *argv[]) {
    int cli_fd, len;

    if (argc != 3){
        printf("Usage: %s <ip> <port>\n", argv[0]);
        exit(1); 
    }

    /* read ip and port */
    char *ip = argv[1];
    int port = atoi(argv[2]);

    /* initialize the buffer */ 
    char buf[MAX_LEN];

    /* connect to the server */
    cli_fd = openTCPSock(ip, port);

    if(cli_fd <0){
        printf("Failed to open socket (rv=%d)\n", cli_fd);
        exit(1);
    }

    /* get the msg from the server */
    while((len = read(cli_fd, buf, sizeof(buf)-1)) > 0){
        setbuf(stdout, NULL);
        buf[len] = 0;
        if(fputs(buf, stdout) == EOF){
            printf("\n Error: fputs error\n");
        }
    }

    closeSock(cli_fd);

    return 0;
}
