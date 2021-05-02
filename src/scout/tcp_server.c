#include <stdbool.h>
#include "scout/tcp_server.h"
#include "scout/scout_api.h"
#include "scout/pack.h"

#ifdef SCOUT_INSTRUCTIONS
#ifndef SCOUT_DYNAMIC_BUFFERS
#ifndef SCOUT_PIC_CODE
static uint8_t gRecvBuffer[SCOUT_HEADER_SIZE + SCOUT_TCP_MAX_MESSAGE];
static uint8_t gSendBuffer[SCOUT_TCP_MAX_MESSAGE];
#endif /* !SCOUT_PIC_CODE */
#endif /* !SCOUT_DYNAMIC_BUFFERS */
#endif /* SCOUT_INSTRUCTIONS */

#if !defined(SCOUT_SLIM_SIZE) || defined(SCOUT_TCP_CLIENT)
int32_t connect_to_tcp_server(sock_fd * clientSock, uint32_t ip, uint16_t port)
{
    struct sockaddr_in addr;

    /* Sanity Check #1 - serverSock should be valid */
    if (clientSock == NULL)
    {
        return STATUS_INVALID_ARGS;
    }

    /* Creat the socket */
    *clientSock = socket(AF_INET, SOCK_STREAM, 0);
    if (*clientSock == -1)
    {
        return STATUS_TCP_SOCK_FAILED;
    }

    /* Bind to the server's address */
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons( port );
    addr.sin_addr.s_addr = htonl( ip );

    if (connect(*clientSock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        return STATUS_TCP_CONNECT_FAILED;
    }

    /* All was OK */
    return STATUS_OK;
}
#endif /* !SCOUT_SLIM_SIZE || SCOUT_TCP_CLIENT */

#if !defined(SCOUT_SLIM_SIZE) || defined(SCOUT_TCP_SERVER)
int32_t open_tcp_server(sock_fd * serverSock, uint16_t port)
{
    struct sockaddr_in addr;

    /* Sanity Check #1 - serverSock should be valid */
    if (serverSock == NULL)
    {
        return STATUS_INVALID_ARGS;
    }

    /* Creat the socket */
    *serverSock = socket(AF_INET, SOCK_STREAM, 0);
    if (*serverSock == -1)
    {
        return STATUS_TCP_SOCK_FAILED;
    }

    /* Bind to the server's address */
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons( port );
    addr.sin_addr.s_addr = htonl( INADDR_ANY );

    if (bind(*serverSock, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        return STATUS_TCP_BIND_FAILED;
    }

    /* Set up the listen queue */
    if (listen(*serverSock, SCOUT_LISTEN_BACKLOG) < 0)
    {
        return STATUS_TCP_LISTEN_FAILED;
    }

    /* All was OK */
    return STATUS_OK;
}
#endif /* !SCOUT_SLIM_SIZE || SCOUT_TCP_SERVER */

uint32_t full_net_recv(sock_fd sock, uint8_t * buffer, uint32_t length)
{
    uint32_t received = 0;
    int res = 0;
    while(length > received)
    {
        res = recv(sock, &buffer[received], length - received, 0);
        if(res <= 0)
        {
            return 0;
        }
        received += (uint32_t)res;
    }
    return received;
}

#if !defined(SCOUT_SLIM_SIZE) || defined(SCOUT_TCP_SEND)
uint32_t full_net_send(sock_fd sock, uint8_t * buffer, uint32_t length)
{
    uint32_t sent = 0;
    int res = 0;
    while(length > sent)
    {
        res = send(sock, &buffer[sent], length - sent, 0);
        if(res <= 0)
        {
            return 0;
        }
        sent += (uint32_t)res;
    }
    return sent;
}
#endif /* !SCOUT_SLIM_SIZE || SCOUT_TCP_SEND */

#ifdef SCOUT_INSTRUCTIONS

void write_output(void * c, uint8_t * buffer, uint32_t length)
{
    output_data_t * ctx = (output_data_t *)c;
    uint32_t usedSize = length < ctx->size - ctx->offset ? length : ctx->size - ctx->offset;

    /* Append it to the send buffer */
    memcpy(ctx->output + ctx->offset, buffer, usedSize);
    ctx->offset += usedSize;
}

void mark_status(void * c, int32_t status)
{
    output_data_t * ctx = (output_data_t *)c;
    ctx->status = status;
}

int32_t start_server_loop(sock_fd serverSock)
{
    struct sockaddr_in clientAddr;
    socklen_t clientAddrSize = sizeof(clientAddr);
    sock_fd clientSock = 0;
    int res;
    scout_header_t header;
    output_data_t ctx;
    uint8_t outputHeader[sizeof(ctx.status) + sizeof(ctx.size)];
    uint8_t * writeHead;

#ifndef SCOUT_DYNAMIC_BUFFERS
    uint8_t * recvBuffer = GLOBAL(RecvBuffer);
    uint8_t * sendBuffer = GLOBAL(SendBuffer);
#else /* SCOUT_DYNAMIC_BUFFERS */
    uint8_t * recvBuffer = (uint8_t *)malloc(SCOUT_HEADER_SIZE + SCOUT_TCP_MAX_MESSAGE);
    uint8_t * sendBuffer = (uint8_t *)malloc(SCOUT_TCP_MAX_MESSAGE);
    ctx.status = STATUS_OK;

    /* Sanity check */
    if(recvBuffer == NULL || sendBuffer == NULL)
    {
        ctx.status = STATUS_ALLOC_FAILED;
        goto exit_loop;
    }
#endif /* ! SCOUT_DYNAMIC_BUFFERS */

    /* Prepare the recv buffer */
    memset(recvBuffer, 0, SCOUT_HEADER_SIZE + SCOUT_TCP_MAX_MESSAGE);
    memset(sendBuffer, 0, SCOUT_TCP_MAX_MESSAGE);
    memset(outputHeader, 0, sizeof(outputHeader));

    /* Endless server loop */
    while(true)
    {
        /* Accept the new client */
        clientSock = accept(serverSock, (struct sockaddr *)&clientAddr, &clientAddrSize);
        if (clientSock < 0)
        {
            ctx.status = STATUS_TCP_ACCECPT_FAILED;
            goto exit_loop;
        }
        ctx.status = STATUS_OK;

        /* Client loop */
        while (ctx.status == STATUS_OK)
        {
            /* Prepare the context */
            ctx.output = sendBuffer;
            ctx.offset = 0;
            ctx.size   = SCOUT_TCP_MAX_MESSAGE;
            ctx.status = STATUS_FAILURE;

            /* Receive the instruction header */
            if (full_net_recv(clientSock, recvBuffer, SCOUT_HEADER_SIZE) != SCOUT_HEADER_SIZE)
            {
                ctx.status = STATUS_TCP_RECV_FAILED;
                continue;
            }

            /* Parse the header to learn the length */
            ctx.status = parse_header(recvBuffer, SCOUT_HEADER_SIZE, &header, false);
            if (ctx.status != STATUS_OK)
            {
                continue;
            }

            /* Basic sanitation */
            if (header.length > SCOUT_TCP_MAX_MESSAGE)
            {
                ctx.status = STATUS_ILLEGAL_LENGTH;
                continue;
            }

            /* Receive the entire instruction */
            if (header.length > 0 &&
			    full_net_recv(clientSock, &recvBuffer[SCOUT_HEADER_SIZE], header.length) != header.length)
            {
                ctx.status = STATUS_TCP_RECV_FAILED;
                continue;
            }

            /* Pass the instruction onward */
            handle_instruction(&ctx, &header, &recvBuffer[SCOUT_HEADER_SIZE]);

            writeHead = outputHeader;
            pack_uint32( &writeHead, ctx.status );
            pack_uint32( &writeHead, ctx.offset );

            /* Send the response back - header */
            if (full_net_send(clientSock, outputHeader, sizeof(outputHeader)) != sizeof(outputHeader))
            {
                ctx.status = STATUS_TCP_SEND_FAILED;
                continue;
            }
            /* Send the response back - data */
            if (ctx.offset > 0 && full_net_send(clientSock, ctx.output, ctx.offset) != ctx.offset)
            {
                ctx.status = STATUS_TCP_SEND_FAILED;
                continue;
            }
        }

        /* Close the current client */
        close(clientSock);
        clientSock = 0;
    }

exit_loop:

    /* Free resources */
    if(clientSock != 0)
    {
        close(clientSock);
        clientSock = 0;
    }

    if(serverSock != 0)
    {
        close(serverSock);
        serverSock = 0;
    }

#ifdef SCOUT_DYNAMIC_BUFFERS
    free(recvBuffer);
    free(sendBuffer);
#endif /* SCOUT_DYNAMIC_BUFFERS */

    return ctx.status;
}
#endif /* SCOUT_INSTRUCTIONS */
