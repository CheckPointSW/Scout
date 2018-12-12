#ifndef __SCOUT__EXTERNAL__DEPS__H__
#define __SCOUT__EXTERNAL__DEPS__H__

#include "flags.h"                /* Project defined, must come first */
#include "scout/architecture.h"   /* Important architecture defines */

/*************************/
/**  LibC Dependencies  **/
/*************************/

#define NULL (0)
typedef addr_t size_t;

void *   memcpy(void * dst, const void * src, size_t size);
void *   memset(void * dst, int value, size_t size);
void *   malloc(size_t size);
void     free(void * ptr);

/***************************/
/**  Socket Dependencies  **/
/***************************/

#define SOCK_STREAM     1
#define SOCK_DGRAM      2

#define AF_INET         2

#define IPPROTO_TCP     6
#define IPPROTO_UDP     17

#define INADDR_ANY      0

struct in_addr
{
    uint32_t        s_addr;
};

struct sockaddr_in
{
    int16_t         sin_family;
    uint16_t        sin_port;
    struct in_addr  sin_addr;
    uint8_t         sin_zero[8];
};

struct sockaddr
{
    uint16_t        sin_family;
    uint8_t         sa_data[14];
};

typedef int         sock_fd;
typedef size_t      socklen_t;

sock_fd socket(int domain, int type, int protocol);
sock_fd bind(sock_fd socket, const struct sockaddr * address, socklen_t address_len);
int     listen(sock_fd sockfd, int backlog);
sock_fd accept(sock_fd sockfd, struct sockaddr * addr, socklen_t * addrlen);
int     connect(sock_fd sockfd, const struct sockaddr * addr, socklen_t addrlen);
int     recv(sock_fd sockfd, void * buf, size_t len, int flags);
int     send(sock_fd sockfd, void * buf, size_t len, int flags);
void    close(sock_fd fd);

#endif // __SCOUT__EXTERNAL__DEPS__H__
