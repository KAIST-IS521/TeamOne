/*
 * SLA chacker: PGP authentication
 */
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/types.h>
#include <regex.h>
#include <gpgme.h>
#include <locale.h>
#include "slalib.h"

#define MAX_LEN 1024
#define REG1 "->"
#define REG2 ">"
#define BEGIN "-----BEGIN PGP MESSAGE-----"
#define END   "-----END PGP MESSAGE-----"
#define UNAME "Happyhacking TeamOne"
#define AUTH_SUCCESS "Username ->"


/* 
 * Some functions come from https://github.com/seiyak/GPGME-sample-code
 * - fail_if_err()
 * - print_data()
 */

#define fail_if_err(err	)                                       \
  do                                                            \
    {                                                           \
      if (err)                                                  \
        {                                                       \
          fprintf (stderr, "%s:%d: %s: %s\n",                   \
                   __FILE__, __LINE__, gpgme_strsource (err),   \
		   gpgme_strerror (err));                       \
          exit(1);                                              \
        }                                                       \
    }                                                           \
  while (0)

/* read gpgme
 * - modify the function in 
     https://github.com/KAIST-IS521/TeamThree/blob/master/slalib/
 */
void read_data_gpgme(char* buffer, int* len, gpgme_data_t data){

	ssize_t nbytes;

        nbytes = gpgme_data_seek (data, 0, SEEK_SET);
        if (nbytes == -1) {
	        fprintf (stderr, "%s:%d: Error in data seek: ",
        	         __FILE__, __LINE__);
	        perror("");
	        exit (1);
        }

        *len = gpgme_data_read(data, (void*) buffer, 4096);

}

void print_data (gpgme_data_t dh)
{
#define BUF_SIZE 512
  char buf[BUF_SIZE + 1];
  int ret;
  
  ret = gpgme_data_seek (dh, 0, SEEK_SET);
  if (ret)
    fail_if_err (gpgme_err_code_from_errno (errno));
  while ((ret = gpgme_data_read (dh, buf, BUF_SIZE)) > 0)
    fwrite (buf, ret, 1, stdout);
  if (ret < 0)
    fail_if_err (gpgme_err_code_from_errno (errno));

  ret = gpgme_data_seek (dh, 0, SEEK_SET);
}

/* passphrase_cb() */
gpgme_error_t passphrase_cb(void *hook, const char *uid_hint, 
                            const char* passphras_info, int last_was_bad,
                            int fd){
    write(fd, (char*)hook, strlen((char*)hook)); 
 
    return 0;
}

/* Error handling */
void handleError(int sock, const char* func, int rv){
    printf("Failed in %s (%d)\n", func, rv);
    closeSock(sock);
    exit(1);
}

/* My custom recvMsgUntil() */
ssize_t recvMsgUntil2(int sock, const char* regex, void* buf, size_t n){
    int len, i;
    char *p = (char*)buf;

    while((len = read(sock, p, n-1)) > 0){
        setbuf(stdout, NULL);
        p[len] = 0;
        if(fputs(p, stdout) == EOF){
            printf("\n Error: fputs error\n");
        }
        for(i=0;i<len;i++){
          if(p[i] == regex[0]) {
              return len;
          } // if '>' go next
        }
    }

    return -1;
}

/* My custom sendMsg() */
int sendMsg2(int sock, const char* buf, size_t n){
    return write(sock, buf, n); 
}

/* My custom handshake() */
int handshake2(int sock, const char* ID, const char* privKeyPath,
              const char* passPath, const char* successMsg){

     int len;
     char buf[MAX_LEN*4];
     char challenge[MAX_LEN*4];
     
     // initialize
     memset(buf, 0, sizeof(buf));
     memset(challenge, 0, sizeof(challenge));

     // 1. send github id
     len = sendMsg2(sock, ID, strlen(ID));

     // 2. receive encrypted and signed challenge from the server
     len = recvMsgUntil2(sock, REG2, (void*)&buf, sizeof(buf)); 

     // Parse signed and encrypted challenge
     char *line = strtok(strdup(buf), "\n");
     char *p_challenge = challenge;
     int is_start = 0;
     int len_challenge = 0;
     while(line){
         if(strcmp(line,BEGIN) == 0) is_start = 1;
         if(is_start == 1){ 
             memcpy(p_challenge, line, strlen(line));
             p_challenge[strlen(line)] = '\n';
             p_challenge += strlen(line)+1;
             len_challenge += strlen(line)+1;
         }
         if(strcmp(line, END) == 0) break;
         line = strtok(NULL, "\n");
     }
     challenge[len_challenge] = '\0';

     // prepare GPG operations
     char passphrase[MAX_LEN];
     FILE *file;
     char ch;
     int cnt = 0;

     // get passphrase from passPath
     file = fopen(passPath, "r");
     if(file){
        while((ch = fgetc(file)) != EOF){
            passphrase[cnt++] = ch ;
        }
        if(ferror(file)){
            return -1;
        }
        fclose(file);
        passphrase[cnt] = '\n';
     }

     // 3. decrypt and verify
     gpgme_ctx_t ctx;
     gpgme_error_t err;
     gpgme_data_t in, out, plain;

     // initialize GPGME
     gpgme_check_version(NULL);
     gpgme_set_locale(NULL, LC_CTYPE, setlocale (LC_CTYPE, NULL));
     err = gpgme_engine_check_version(GPGME_PROTOCOL_OpenPGP);
     fail_if_err(err);
 
     // initialize GPGME context
     err = gpgme_new(&ctx);
     fail_if_err(err);
     
     // set engine information
     err = gpgme_ctx_set_engine_info(ctx, GPGME_PROTOCOL_OpenPGP,
                                     "/usr/bin/gpg",
                                     "/home/vagrant/.gnupg");
     fail_if_err(err);

     // set armor
     gpgme_set_armor(ctx, 1);

     // convert the challenge to gpgme_data
     err = gpgme_data_new_from_mem(&in, challenge, len_challenge, 0);
     fail_if_err(err);

#if 1
     // include signature within key
     gpgme_keylist_mode_t kmode = gpgme_get_keylist_mode(ctx);
     kmode |= GPGME_KEYLIST_MODE_SIGS;
     err = gpgme_set_keylist_mode(ctx, kmode);
     fail_if_err(err);
     // get public key list  
     gpgme_key_t pkey[2] = {NULL, NULL};
     err = gpgme_op_keylist_start(ctx, 0, 0);
     while((gpgme_op_keylist_next(ctx, &pkey[0]) != GPG_ERR_EOF) 
            && pkey[0]){
         if(strcmp(UNAME, pkey[0]->uids->name) == 0)
             break;
     }
#endif
     // set passphrase to ctx
     gpgme_set_passphrase_cb(ctx, passphrase_cb, (void*)passphrase);

     // import my private key for decryption
     gpgme_data_t key_data;
     int key_fd = open(privKeyPath, O_RDONLY);
     if(key_fd == -1) return -6;

     err = gpgme_data_new_from_fd(&key_data, key_fd);
     fail_if_err(err);
 
     err = gpgme_op_import(ctx, key_data);
     gpgme_data_release(key_data);
     fail_if_err(err);

     // decrypt and verify
     err = gpgme_data_new(&plain);
     fail_if_err(err);

     err = gpgme_data_new(&out);
     fail_if_err(err);

     gpgme_data_seek(in, 0, SEEK_SET);
     err = gpgme_op_decrypt_verify(ctx, in, plain);
     fail_if_err(err);

     gpgme_op_decrypt_result(ctx);
     gpgme_data_seek(plain, 0, SEEK_SET);
  
     // encrypt the random using the server key
     err = gpgme_op_encrypt(ctx, pkey, GPGME_ENCRYPT_ALWAYS_TRUST, 
                            plain, out);
     fail_if_err(err);

     gpgme_op_encrypt_result(ctx);
     char buffer[MAX_LEN*4];
     int enc_len = 0;
     memset(buffer, 0, sizeof(buffer));
     read_data_gpgme(buffer, &enc_len, out);
     
     // 4. send the encrypted response to the server
     len = sendMsg2(sock, buffer, enc_len);

     // 5. receive the registration menu if the authentication is succeed
     len = recvMsgUntil2(sock, REG2, (void*)&buf, sizeof(buf));

     // Parse the received buffer
     line = strtok(strdup(buf), "\n");
     int is_succeed = 0;
     while(line){
         if(strstr(line,successMsg) != NULL){
             is_succeed = 1;
             break;
         }
         line = strtok(NULL, "\n");
     }

     if(is_succeed == 0)
         return -1;
 
     // finalizae
     close(key_fd);
     gpgme_release(ctx);

     return len;
}

/* hexdump() from https://gist.github.com/ccbrown/9722406 */
void hexdump(const void* data, size_t size) {
    char ascii[17];
    size_t i, j;
    ascii[16] = '\0';
    for (i = 0; i < size; ++i) {
        printf("%02X ", ((unsigned char*)data)[i]);
        if (((unsigned char*)data)[i] >= ' ' 
            && ((unsigned char*)data)[i] <= '~') {
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
    int rv;

    if (argc != 6){
        printf(
            "Usage: %s <ip> <port> <github_id> <privPath> <passPath>\n", 
             argv[0]);
        exit(1); 
    }

    /* read ip and port */
    char *ip = argv[1];
    int port = atoi(argv[2]);
    char *ID = argv[3];
    char *privKey = argv[4];
    char *pass = argv[5];

    /* initialize the buffer */ 
    char buf[MAX_LEN];

    /* connect to the server */
    cli_fd = openTCPSock(ip, port);

    if(cli_fd <0){
        printf("Failed to open socket (rv=%d)\n", cli_fd);
        exit(1);
    }

    /* get the initial msg from the server */
    printf("<<< Receiving the initial msg from the server...\n");
    len = recvMsgUntil2(cli_fd, REG2, (void*)&buf, sizeof(buf));
    if(len < 0){
        handleError(cli_fd, "recvMsgUntil", len);
    }

    /* send the menu for registration */
    printf(">>> Sending the menu selection to the server...\n");
    len = sendMsg2(cli_fd, "2\n", strlen("2\n"));
    if(len < 0){
        handleError(cli_fd, "sendMsg", len);
    }

    /* get the msg from the server */
    printf("<<< Receiving the msg from the server...\n");
    len = recvMsgUntil2(cli_fd, REG2, (void*)&buf, sizeof(buf));
    if(len < 0){
        handleError(cli_fd, "recvMsgUntil", len);
    }

    /* process PGP authentication */
    char github_id[MAX_LEN];
    memset(github_id, 0, sizeof(github_id));
    sprintf(github_id, "%s\n", ID);
    rv = handshake2(cli_fd, github_id, privKey, pass, AUTH_SUCCESS);
    if(rv < 0){
        handleError(cli_fd, "handshake", rv);
    }
 
    closeSock(cli_fd);

    return 0;
}
