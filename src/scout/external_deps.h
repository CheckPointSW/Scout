#ifndef __SCOUT__EXTERNAL__DEPS__H__
#define __SCOUT__EXTERNAL__DEPS__H__

#include "flags.h"                /* Project defined, must come first */
#include "scout/architecture.h"   /* Important architecture defines */

#ifdef SCOUT_ISOLATED_ENV

/*************************/
/**  LibC Dependencies  **/
/*************************/

#define NULL (0)
typedef addr_t size_t;
typedef size_t off_t;

#ifndef SCOUT_SLIM_SIZE

void *   memcpy(void * dst, const void * src, size_t size);
void *   memset(void * dst, int value, size_t size);
void *   malloc(size_t size);
void     free(void * ptr);

#endif /* SCOUT_SLIM_SIZE */

/***************************/
/**  Socket Dependencies  **/
/***************************/

#if defined(SCOUT_HOST_GLIBC)

#define SOCK_STREAM     1
#define AF_INET         2

#define IPPROTO_TCP     6
#define IPPROTO_UDP     17

#define INADDR_ANY      0

#elif defined(SCOUT_HOST_UCLIBC)

#define SOCK_STREAM     2
#define AF_INET         2

#define IPPROTO_TCP     6
#define IPPROTO_UDP     17

#define INADDR_ANY      0

#endif

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

#ifndef SCOUT_SLIM_SIZE

sock_fd socket(int domain, int type, int protocol);
sock_fd bind(sock_fd socket, const struct sockaddr * address, socklen_t address_len);
int     listen(sock_fd sockfd, int backlog);
sock_fd accept(sock_fd sockfd, struct sockaddr * addr, socklen_t * addrlen);
int     connect(sock_fd sockfd, const struct sockaddr * addr, socklen_t addrlen);
int     recv(sock_fd sockfd, void * buf, size_t len, int flags);
int     send(sock_fd sockfd, void * buf, size_t len, int flags);
void    close(sock_fd fd);

#endif /* SCOUT_SLIM_SIZE */

/*************************/
/**  MMap Dependencies  **/
/*************************/
#if defined(SCOUT_HOST_GLIBC)

#define PROT_READ       0x01
#define PROT_WRITE      0x02
#define PROT_EXEC       0x04


#define MAP_PRIVATE     0x02
#define MAP_FIXED       0x10
#define MAP_ANONYMOUS   0x20

#elif defined(SCOUT_HOST_UCLIBC)

#define PROT_READ       0x01
#define PROT_WRITE      0x02
#define PROT_EXEC       0x04

#define MAP_PRIVATE     0x02
#define MAP_FIXED       0x10
#define MAP_ANONYMOUS	0x800

#endif

#ifndef SCOUT_SLIM_SIZE

void * mmap(void * addr, size_t length, int prot, int flags, int fd, off_t offset);
int    mprotect(void * addr, size_t len, int prot);
int    munmap(void * addr, size_t length);

#endif /* SCOUT_SLIM_SIZE */

#endif /* SCOUT_ISOLATED_ENV */

#endif // __SCOUT__EXTERNAL__DEPS__H__
