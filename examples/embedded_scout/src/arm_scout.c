#include "arm_scout.h"
#include "scout/tcp_server.h"

void main()
{
    sock_fd serverSock;
    int32_t status;

    /* Open the TCP server */
    status = open_tcp_server(&serverSock, SCOUT_PORT);
    if (status != STATUS_OK)
    {
        goto free_resources;
    }

    /* Register the supported instructions */
    register_all_instructions();

    /* Activate the TCP server */
    status = start_server_loop(serverSock);

free_resources:
    /* nothing to be done for now */
    return;
}
