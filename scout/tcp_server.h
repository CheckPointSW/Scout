#ifndef __SCOUT__TCP__SERVER__H__
#define __SCOUT__TCP__SERVER__H__

/***********************/
/**  Network Configs  **/
/***********************/

#define SCOUT_PORT              0x2562
#define SCOUT_LOADER_PORT       0x2561
#define SCOUT_LISTEN_BACKLOG    5
#define SCOUT_TCP_MAX_MESSAGE   0x1000

#include "scout/scout.h" // Depdendecy cycle in PIC mode forces us to include this file only at this line

#ifdef SCOUT_PC_ENV
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <netinet/in.h>
#include <unistd.h>

typedef int sock_fd;
#endif /* SCOUT_PC_ENV */

/***************/
/**  Structs  **/
/***************/

typedef struct __output_data
{
    uint8_t *   output;
    uint16_t    offset;
    uint32_t    size;
    int32_t     status;
} output_data_t;

/*****************/
/**  Functions  **/
/*****************/

/**
 * Connects to a remote TCP server
 *
 * @author eyalit (03/05/2018)
 *
 * @param serverSock - pointer to the created server socket
 * @param ip - remote ip to be used
 * @param port - tcp port to be used
 *
 * @return int32_t - success status
 */
int32_t connect_to_tcp_server(sock_fd * serverSock, uint32_t ip, uint16_t port);

/**
 * Creates a TCP server for receiving instructions
 *
 * @author eyalit (08/03/2018)
 *
 * @param serverSock - pointer to the created server socket
 * @param port - tcp port to be used
 *
 * @return int32_t - success status
 */
int32_t open_tcp_server(sock_fd * serverSock, uint16_t port);

/**
 * Starts the endless loop of the server socket.
 *
 * @author eyalit (08/03/2018)
 *
 * @param serverSock - socket descriptor for the server
 *
 * @return int32_t - success status
 */
int32_t start_server_loop(sock_fd serverSock);

/**
 * A reliable packet receive over a stream.
 *
 * @author eyalit (08/03/2018)
 *
 * @param sock - socket descriptor for the stream
 * @param buffer - buffer for the incoming data
 * @param length - number of bytes to be received
 *
 * @return uint32_t - number of received bytes
 */
uint32_t full_net_recv(sock_fd sock, uint8_t * buffer, uint32_t length);

/**
 * A reliable packet send over a stream.
 *
 * @author eyalit (08/03/2018)
 *
 * @param sock - socket descriptor for the stream
 * @param buffer - buffer for the outgoing data
 * @param length - number of bytes to be sent
 *
 * @return uint32_t - number of sent bytes
 */
uint32_t full_net_send(sock_fd sock, uint8_t * buffer, uint32_t length);

#endif // __SCOUT__TCP__SERVER__H__
