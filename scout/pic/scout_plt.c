#include "scout/pic/pic_wrapper.h"

#ifdef SCOUT_PIC_CODE

/* LibC */
void * memcpy(void * dst, const void * src, size_t size)
{
    return ((void * (*)(void *, const void *, size_t))get_context()->functions.scout.memcpy)(dst, src, size);
}

void * memset(void * dst, int value, size_t size)
{
    return ((void * (*)(void *, int, size_t))get_context()->functions.scout.memset)(dst, value, size);
}

void * malloc(size_t size)
{
    return ((void * (*)(size_t))get_context()->functions.scout.malloc)(size);
}

void free(void * ptr)
{
    ((void (*)(void *))get_context()->functions.scout.free)(ptr);
}

/* Sockets */
sock_fd socket(int domain, int type, int protocol)
{
    return ((sock_fd (*)(int, int, int))get_context()->functions.scout.socket)(domain, type, protocol);
}

sock_fd bind(sock_fd socket, const struct sockaddr * address, socklen_t address_len)
{
    return ((sock_fd (*)(sock_fd, const struct sockaddr *, socklen_t))get_context()->functions.scout.bind)(socket, address, address_len);
}

int listen(sock_fd sockfd, int backlog)
{
    return ((int (*)(sock_fd, int))get_context()->functions.scout.listen)(sockfd, backlog);
}

sock_fd accept(sock_fd sockfd, struct sockaddr * addr, socklen_t * addrlen)
{
    return ((sock_fd (*)(sock_fd, struct sockaddr *, socklen_t *))get_context()->functions.scout.accept)(sockfd, addr, addrlen);
}

int connect(sock_fd sockfd, const struct sockaddr * addr, socklen_t addrlen)
{
    return ((int (*)(sock_fd, const struct sockaddr *, socklen_t))get_context()->functions.scout.connect)(sockfd, addr, addrlen);
}

int recv(sock_fd sockfd, void * buf, size_t len, int flags)
{
    return ((int (*)(sock_fd, void *, size_t, int))get_context()->functions.scout.recv)(sockfd, buf, len, flags);
}

int send(sock_fd sockfd, void * buf, size_t len, int flags)
{
    return ((int (*)(sock_fd, void *, size_t, int))get_context()->functions.scout.send)(sockfd, buf, len, flags);
}

void close(sock_fd fd)
{
    ((void (*)(sock_fd))get_context()->functions.scout.close)(fd);
}

#ifdef SCOUT_MMAP

void * mmap(void * addr, size_t length, int prot, int flags, int fd, off_t offset)
{
    return ((void * (*)(void *, size_t, int, int, int, off_t))get_context()->functions.scout.mmap)(addr, length, prot, flags, fd, offset);
}

int mprotect(void * addr, size_t len, int prot)
{
    return ((int (*)(void *, size_t, int))get_context()->functions.scout.mprotect)(addr, len, prot);
}

int munmap(void * addr, size_t length)
{
    return ((int (*)(void *, size_t))get_context()->functions.scout.munmap)(addr, length);
}

#endif /* SCOUT_MMAP */

#endif /* SCOUT_PIC_CODE */
