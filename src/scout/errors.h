#ifndef __SCOUT__ERROR__H__
#define __SCOUT__ERROR__H__

/* General Statuses */
#define STATUS_OK                     0
#define STATUS_FAILURE                1
#define STATUS_INVALID_ARGS           2
#define STATUS_ALLOC_FAILED           3
#define STATUS_TCP_SOCK_FAILED        4
#define STATUS_TCP_BIND_FAILED        5
#define STATUS_TCP_LISTEN_FAILED      6
#define STATUS_TCP_ACCECPT_FAILED     7
#define STATUS_TCP_CONNECT_FAILED     8
#define STATUS_TCP_RECV_FAILED        9
#define STATUS_TCP_SEND_FAILED       10

/* Scout API Statuses */
#define STATUS_SMALL_HEADER          20
#define STATUS_ILLEGAL_LENGTH        21
#define STATUS_ILLEGAL_INSTR_ID      22

#endif /* __SCOUT__ERROR__H__ */
