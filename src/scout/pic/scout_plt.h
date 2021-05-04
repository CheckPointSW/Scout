#ifndef __SCOUT__PIC__PLT__H__
#define __SCOUT__PIC__PLT__H__

#include "scout/scout.h"

#ifdef SCOUT_PIC_CODE

/***************/
/**  Structs  **/
/***************/

typedef struct __pic_got
{
    /* LibC */
    addr_t      memcpy;
    addr_t      memset;
    addr_t      malloc;
    addr_t      free;
    /* Sockets */
    addr_t      socket;
    addr_t      bind;
    addr_t      listen;
    addr_t      accept;
    addr_t      connect;
    addr_t      recv;
    addr_t      send;
    addr_t      close;
#ifdef SCOUT_MMAP
    /* MMap */
    addr_t      mmap;
    addr_t      mprotect;
    addr_t      munmap;
#endif /* SCOUT_MMAP */
} pic_got_t;

/**
 * If we are short in size (PIC loader), we will have special treatment for the default
 * GOT/PLT of Scout itself (without the extensions). As we don't have strings in the code
 * when it is under tight size constraints, this solution should be relatively robust.
 *
 * This way we would save the redundant assembly instructions of loading all arguments to
 * registers, calling a PLT function, and then saving them all aside because we first need
 * to fetch the context, and only then we need to use them for invoking the real function.
 *
 * Here is an example from the PLT record of accept in an ARM compilation:
 *  .text:00008284                      EXPORT accept
 *  .text:00008284                      accept
 *  .text:00008284 0D C0 A0 E1          MOV     R12, SP
 *  .text:00008288 F0 D8 2D E9          PUSH    {R4-R7,R11,R12,LR,PC}
 *  .text:0000828C 04 B0 4C E2          SUB     R11, R12, #4
 *  .text:00008290 00 40 A0 E1          MOV     R4, R0
 *  .text:00008294 01 50 A0 E1          MOV     R5, R1
 *  .text:00008298 02 60 A0 E1          MOV     R6, R2
 *  .text:0000829C 64 FF FF EB          BL      get_context
 *  .text:000082A0 06 20 A0 E1          MOV     R2, R6
 *  .text:000082A4 1C 30 90 E5          LDR     R3, [R0,#0x1C]
 *  .text:000082A8 05 10 A0 E1          MOV     R1, R5
 *  .text:000082AC 04 00 A0 E1          MOV     R0, R4
 *  .text:000082B0 1C D0 4B E2          SUB     SP, R11, #0x1C
 *  .text:000082B4 F0 68 9D E8          LDMFD   SP, {R4-R7,R11,SP,LR}
 *  .text:000082B8 13 FF 2F E1          BX      R3
 *  .text:000082B8                      ; End of function accept
 *
 * Our solution will use dedicated macros, that will fetch the context prior to invoking
 * the function, thus saving these wasted instructions.
 */
#ifdef SCOUT_SLIM_SIZE

/* LibC */
#define memcpy(_D_, _S_, _L_)  \
    (void * (*)(void *, const void *, size_t))get_context()->functions.scout.memcpy)(_D_, _S_, _L_)

#define memset(_D_, _V_, _S_)  \
    ((void * (*)(void *, int, size_t))get_context()->functions.scout.memset)(_D_, _V_, _S_)

#define malloc(_S_)  \
    ((void * (*)(size_t))get_context()->functions.scout.malloc)(_S_)

#define free(_P_)  \
    (((*)(void *))get_context()->functions.scout.free)(_P_)

/* Sockets */
#define socket(_D_, _T_, _P_)  \
    ((sock_fd (*)(int, int, int))get_context()->functions.scout.socket)(_D_, _T_, _P_)

#define bind(_S_, _A_, _L_)  \
    ((sock_fd (*)(sock_fd, const struct sockaddr *, socklen_t))get_context()->functions.scout.bind)(_S_, _A_, _L_)

#define listen(_S_, _B_)  \
    ((int (*)(sock_fd, int))get_context()->functions.scout.listen)(_S_, _B_)

#define accept(_S_, _A_, _L_)  \
    ((sock_fd (*)(sock_fd, struct sockaddr *, socklen_t *))get_context()->functions.scout.accept)(_S_, _A_, _L_)

#define connect(_S_, _A_, _L_)  \
    ((int (*)(sock_fd, const struct sockaddr *, socklen_t))get_context()->functions.scout.connect)(_S_, _A_, _L_)

#define recv(_S_, _B_, _L_, _F_)  \
    ((int (*)(sock_fd, void *, size_t, int))get_context()->functions.scout.recv)(_S_, _B_, _L_, _F_)

#define send(_S_, _B_, _L_, _F_)  \
    ((int (*)(sock_fd, void *, size_t, int))get_context()->functions.scout.send)(_S_, _B_, _L_, _F_)

#define close(_F_)  \
    ((void (*)(sock_fd))get_context()->functions.scout.close)(_F_)

#ifdef SCOUT_MMAP

#define mmap(_A_, _L_, _P_, _F_, _FD_, _O_)  \
    ((void * (*)(void *, size_t, int, int, int, off_t))get_context()->functions.scout.mmap)(_A_, _L_, _P_, _F_, _FD_, _O_)

#define mprotect(_A_, _L_, _P_)  \
    ((int (*)(void *, size_t, int))get_context()->functions.scout.mprotect)(_A_, _L_, _P_)

#define munmap(_A_, _L_)  \
    ((int (*)(void *, size_t))get_context()->functions.scout.munmap)(_A_, _L_)

#endif /* SCOUT_MMAP */

#endif /* SCOUT_SLIM_SIZE */

#endif /* SCOUT_PIC_CODE */

#endif // __SCOUT__PIC__PLT__H__
