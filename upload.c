#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <mysql/mysql.h>
#include <netinet/in.h>
#include <pthread.h>
#include <netdb.h>  /* netdb is necessary for struct hostent */
#include <arpa/inet.h>
#define PORT 5555
#define MAX_THREAD 5
#define BUF_LEN 4096
#define MYSQL_HOST "127.0.0.1"
#define MYSQL_USER "root"
#define MYSQL_PORT 3306
#define DB "statisticsd"

MYSQL conn;
pthread_mutex_t mysql_lock;

struct worker{
    void * args;
    struct worker * next;
}thread_worker;

struct{
    pthread_mutex_t queue_lock;
    pthread_cond_t queue_ready;
    pthread_t * threadid;
    int cur_queue_size;
    struct worker * worker_head;

    int canwork_num;
}pool;

MYSQL_RES * mysql_select(char * cmd){
    printf("%s\n", cmd);
    MYSQL_RES * res;
    if(mysql_query(&conn, cmd)){
        printf("mysql select error");
        exit(1);
    }
    if(!(res = mysql_store_result(&conn))){
        printf("get result error!");
        exit(1);
    }
    return res;
}

void mysql_update(char * cmd){
    printf("%s\n", cmd);
    if(mysql_query(&conn, cmd)){
        printf("update error\n");
        exit(1);
    }
    mysql_commit(&conn);
    return;
}

void mysql_insert(char * cmd){
    printf("%s\n", cmd);
    if(mysql_query(&conn, cmd)){
        printf("mysql insert error");
        exit(1);
    }
    mysql_commit(&conn);
}

int check(void *buf, int len){
    if(len <= 33){
        return 0;
    }
    char * p = (char *)buf;
    int i = 0;
    for(; i< len; i++){
        if(p[i] == ';' && (i != len-1)){
            i++;
            for(; i < len; i++){
                if(p[i] < '0' || p[i] > '9'){
                    return 0;
                }
            }
            return 1;
        }
    }

    return 0;
}

void recv_file(void * ff, void * buf)
{
    int fd = *(int *)(ff);
    struct timeval timeout = {10, 0};
    setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));
    int len;
    int write_len = 0;
    int recv_len;
    char *msg_len;
    char filename[255];
    char query[500];
    MYSQL_RES * res;
    MYSQL_ROW row;
    bzero(buf, BUF_LEN);
    int uploaded = 0;
    if((len = recv(fd, buf, BUF_LEN, 0)) == -1)       //这个接收关于文件的信息， 格式为 md5;length
    {
        perror("recv error: ");
        close(fd);
        return;
    }

    if(check(buf, len) == 0){
        close(fd);
        printf("md5;length error\n");
        return;
    }
    strtok((char *)buf, ";");
    sprintf(filename , "%s", buf);
    msg_len = strtok(NULL, ";");
    len = strlen(msg_len);
    msg_len[len] = '\0';
    len = atoi(msg_len);
    printf("len: %d\n", len);

    pthread_mutex_lock(&mysql_lock);
    sprintf(query, "select * from up_file where md5 = '%s'" , filename);
    res = mysql_select(query);
    if(mysql_num_rows(res) == 1){
        uploaded = 1;
        row =  mysql_fetch_row(res);
        printf("up_size: %s\n", row[3]);
        write_len = atoi(row[3]);
    }else{
        printf("have zero\n");
    }
    mysql_free_result(res);
    pthread_mutex_unlock(&mysql_lock);

    bzero(buf, BUF_LEN);
    sprintf(buf, "%d", write_len);
    send(fd, buf, strlen(buf), 0);                  //发送postion
    bzero(buf, BUF_LEN);

    FILE *fp;
    printf("filename: %s\n", filename);
    if((fp = fopen(filename, "ab")) == NULL){
        perror("open error: ");
        return;
    }
    while(1){
        recv_len = recv(fd, buf, BUF_LEN, 0);
        if(recv_len == -1){
            perror("recv error: ");
            pthread_mutex_lock(&mysql_lock);
            if(uploaded){
                sprintf(query, "update up_file set up_size = %d where md5 = '%s'", write_len, filename);
                mysql_update(query);
                
            }else{
                sprintf(query, "insert into up_file values(NULL, '%s', %d, %d)", filename, len, write_len);
                mysql_insert(query);
            }
            pthread_mutex_unlock(&mysql_lock);
            break;
        }
        if(recv_len == 0){                              //recv_len==0 为客户端断开连接，判断是否接收完文件，并把数据写进数据库
            printf("recv success: %d\n", write_len);
            pthread_mutex_lock(&mysql_lock);
            if(uploaded){
                sprintf(query, "update up_file set up_size = %d where md5 = '%s'", write_len, filename);
                mysql_update(query);
                
            }else{
                sprintf(query, "insert into up_file values(NULL, '%s', %d, %d)", filename, len, write_len);
                mysql_insert(query);
            }
            pthread_mutex_unlock(&mysql_lock);
            break;
        }

        if(recv_len != -1){
            //printf("len : %d\n", recv_len);
            fwrite(buf, sizeof(char), recv_len , fp);
            write_len += recv_len;
        }
        
    }
    close(fd);
    fclose(fp);
}

void * thread_route(){
    void * buf = malloc(BUF_LEN);
    
    while(1){
        pthread_mutex_lock(&(pool.queue_lock));       //加锁
        while(pool.cur_queue_size == 0){
            pthread_cond_wait(&(pool.queue_ready), &(pool.queue_lock));
        }
        struct worker * pwork = pool.worker_head;
        pool.worker_head = pool.worker_head->next;
        pool.cur_queue_size--;
        pool.canwork_num--;
        pthread_mutex_unlock(&(pool.queue_lock));       //解锁

        printf("my thread id: %x\n", pthread_self());
        //处理客户端连接的代码
        
        recv_file(pwork->args, buf);
        
        free(pwork);
        pwork = NULL;

        pthread_mutex_lock(&(pool.queue_lock));
        pool.canwork_num++;
        printf("can_work: %d\n", pool.canwork_num);
        pthread_mutex_unlock(&(pool.queue_lock));
    }
}

void thread_pool_init(){
    bzero(&pool, sizeof(pool));
    pthread_mutex_init(&(pool.queue_lock), NULL);
    pthread_cond_init(&(pool.queue_ready), NULL);
    pool.cur_queue_size= 0;
    pool.worker_head = NULL;
    pool.canwork_num = MAX_THREAD;

    pool.threadid = (pthread_t *)malloc(MAX_THREAD * sizeof(pthread_t));
    int i = 0;
    for(; i < MAX_THREAD; i++){
        pthread_create(&(pool.threadid[i]), NULL, thread_route, NULL);
    }
}

int add_work(void * args){
    struct worker * newwork = (struct worker*)malloc(sizeof(struct worker));
    struct worker * tmp = NULL;
    newwork->args = args;
    newwork->next = NULL;

    pthread_mutex_lock(&(pool.queue_lock));
    
    tmp = pool.worker_head;
    if(tmp != NULL){
        while(tmp->next != NULL)
            tmp = tmp->next;
        tmp->next = newwork;
    }else{
        pool.worker_head = newwork;
    }
    pool.cur_queue_size++;

    pthread_mutex_unlock(&(pool.queue_lock));

    pthread_cond_signal(&(pool.queue_ready));
    return 0;
}


void conn_mysql(){
    int ret;

    mysql_init(&conn);
    if(mysql_real_connect(&conn, MYSQL_HOST, MYSQL_USER, "root", DB, 3306, NULL, 0)){
        perror("mysql error: ");
    }

}

void  * keeplive(){
    MYSQL_RES * res;
    
    while(1){
        printf("eeeeeee\n");
        pthread_mutex_lock(&mysql_lock);
        if(mysql_query(&conn, "select now()")){
            printf("mysql断开\n");
            if(mysql_ping(&conn)){
                conn_mysql();
            }
        }
        res = mysql_store_result(&conn);
        mysql_free_result(res);

        pthread_mutex_unlock(&mysql_lock);
        sleep(300);
    }
}

int main(){
    struct sockaddr_in server; /* server's address information */
    struct sockaddr_in client; /* client's address information */
    int listenfd;
    int client_sock;
    pthread_t id;
    socklen_t addrlen;
    if((listenfd=socket(AF_INET,SOCK_STREAM, 0))==-1){
        perror("socket() error\n");
        exit(1);
    }
    int opt = SO_REUSEADDR;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    bzero(&server, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);
    server.sin_addr.s_addr = inet_addr("0.0.0.0");
    addrlen = sizeof(server);
    if(bind(listenfd, (struct sockaddr *)&server, sizeof(server)) == -1)
        perror("bind error");

    if(listen(listenfd, MAX_THREAD) == -1){
        perror("listen error\n");
        exit(1);
    }
    thread_pool_init();
    
    //pthread_create(NULL, NULL, keeplive, NULL);
    conn_mysql();
    pthread_create(&id, NULL, keeplive, NULL);

    while(1){
        if( (client_sock = accept(listenfd, (struct sockaddr *)&client, &addrlen)) == -1){
            perror("accept error: ");
            continue;
        }
        add_work(&client_sock);
    }
}
