#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>

#include "scout_user.h"
#include "scout/tcp_server.h"
#include "scout/scout_api.h"

#define KERNEL_IOCTL_HEADER  (2 * sizeof(addr_t))

int driverFD = -1;
volatile uint8_t dataStream[1024] = {0};
volatile control_stream_t stats = {0, 0};

void register_specific_instructions(void)
{
    /* No instruction to be registerred */
}

int32_t handle_instruction(void * ctx, scout_header_t * header, uint8_t * instruction)
{
	int32_t status;
	output_data_t * output = (output_data_t *)ctx;
    uint32_t length = header->length;
	uint8_t * buffer = (uint8_t *)malloc(KERNEL_IOCTL_HEADER + sizeof(scout_header_t) + length);
    /* Check for failure */
	if (buffer == NULL)
	{
		printf("Failed to allocate a buffer of size %d\n", KERNEL_IOCTL_HEADER + sizeof(scout_header_t) + length);
		return STATUS_FAILURE;
	}

	/* Place the stream header */
	((addr_t *)buffer)[0] = (addr_t)dataStream;
	((addr_t *)buffer)[1] = (addr_t)&stats;

    /* Now place the scout header */
    memcpy(&buffer[KERNEL_IOCTL_HEADER], header, sizeof(scout_header_t));

	/* Copy the data itself */
	memcpy(&buffer[KERNEL_IOCTL_HEADER + sizeof(scout_header_t)], instruction, length);

    /* Send the instruction onward to the scout driver */
	ioctl(driverFD, KERNEL_IOCTL_HEADER + sizeof(scout_header_t) + length, buffer);
	status = stats.status;

	/* Don't forget to pass on the output */
    write_output(output, (uint8_t *)dataStream, stats.written);
    mark_status(output, stats.status);

	/* Free the buffer */
	free(buffer);
	buffer = NULL;

	return status;
}

int main(int argc, char** argv)
{
	sock_fd serverSock;
	int32_t status;

    /* Open the scout driver */
	printf("Opening the file\n");
	driverFD = open("/dev/KernelScout", O_RDWR);
	if ( driverFD == -1 )
	{
		perror("Failed to open the driver... ");
		exit(1);
	}
	printf("Successfully opened the driver: fd = %d\n", driverFD);

	/* Open the TCP server */
	status = open_tcp_server(&serverSock, SCOUT_PORT);
	if(status != STATUS_OK)
	{
		printf("Failed to open the TCP proxy server, status = %d\n", status);
		goto free_resources;
	}

	/* Activate the TCP server */
	status = start_server_loop(serverSock);

free_resources:

	printf("press any key to continue...\n");
	fgetc(stdin);
	return 0;
}
