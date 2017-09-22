#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <netdb.h>  /* netdb is necessary for struct hostent */
#include <arpa/inet.h>
#include <sys/stat.h>
int main(int args, char *argv[]){
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    char buf[4096];
    char path[500];
    sprintf(path, "%s" ,argv[1]);
    int pos;
    struct sockaddr_in client;

    bzero(buf, 4096);
    sprintf(buf, "md5sum %s", path);
    printf("file: %s\n", buf);
    FILE * md5 = popen(buf, "r");
    bzero(buf, 4096);
    fgets(buf, 33, md5);
    fclose(md5);
    printf("md5: %s\n", buf);

    FILE * fp;
    if((fp = fopen(path, "rb")) == NULL){
        perror("open error: ");
        exit(1);
    }
    int len;
    int readlen = 0;
    
    struct stat statbuf;  
    stat(path, &statbuf);  
    int size =statbuf.st_size; 
    if(size == 0){
        printf("file size: 0?");
        exit(1);
    }
    sprintf(buf, "%s;%d", buf, size);

    printf("%s\n", buf);

    client.sin_family = AF_INET;
    client.sin_port = htons(5555);
    client.sin_addr.s_addr = inet_addr("10.0.0.214");

    socklen_t clen = sizeof(client);
    if(connect(fd, (struct sockaddr*)&client, clen) == -1){
        perror("connect error: ");
        exit(-1);
    }
    
    send(fd, buf, strlen(buf), 0);    //发送文件大小
    bzero(buf, 4096);
    recv(fd, buf, 4096, 0);           //从upload返回的postion，从这个位置开始上传
    pos = atoi(buf);
    if(pos == size){
        printf("exists file\n");
        exit(1);
    }
    printf("pos: %d\n", pos);
    fseek(fp, pos, 0);
    while(len = fread(buf, sizeof(char), 4096, fp)){
        if(len == -1){
            perror("read error: ");
            close(fd);
            exit(1);
        }else if(len == 0){
            printf("send success");
            break;
        }else{
            send(fd, buf, len, 0);
            readlen += len;
        }
    }
    printf("readlen : %d\n", readlen);
    close(fd);
    return 0;
}
