#include <linux/init.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/mm.h>
#include <linux/dma-mapping.h>
#include <linux/slab.h>
#include <linux/device.h>

/* Scout headers */
#include "scout/scout.h"
#include "scout/scout_api.h"
/* Kernel Scout Instructions */
#include "scout_kernel_instructions.h"

/******************************/
/**  Driver Headers & Funcs  **/
/******************************/

#define DEVICE_NAME "KernelScout"
#define CLASS_NAME  "KernelScout"

static int majorNumber = 0;
static struct class* scoutClass = NULL;

static int dev_open(struct inode *, struct file *);
static int dev_release(struct inode *, struct file *);
int scout_ioctl(struct file *file, unsigned int cmd, unsigned long arg);

void scout_open(void);
void write_output(void * c, uint8_t * buffer, uint32_t length);
void mark_status(void * c, int32_t status);

#define SCOUT_LOG(SEV, MESSAGE, ...)	printk(SEV MESSAGE, ##__VA_ARGS__)

/*************************/
/**  Scout Actual Code  **/
/*************************/

void scout_open(void)
{
	/* Register all of the supported instructions */
	register_all_instructions();
}

void write_output(void * c, uint8_t * buffer, uint32_t length)
{
	scout_kernel_ctx_t * ctx = (scout_kernel_ctx_t *)c;
	/* Copy the output back to the user */
	copy_to_user(&ctx->output[ctx->written], buffer, length);
	/* Sum up the written buffer */
	ctx->written += length;

	SCOUT_LOG(KERN_INFO, "write_output() with size = %d, data = 0x%p\n", length, ((void**)buffer)[0]);
}

void mark_status(void * c, int32_t status)
{
	scout_kernel_ctx_t * ctx = (scout_kernel_ctx_t *)c;
	ctx->status = status;

    /* Pass the output to the user */
	copy_to_user(ctx->stats, &status, sizeof(status));
	copy_to_user(&ctx->stats[1], &ctx->written, sizeof(ctx->written));

	SCOUT_LOG(KERN_INFO, "mark_status() with status = %d, written = %d\n", ctx->status, ctx->written);
}

int scout_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
	uint8_t __user *p = (uint8_t __user *)arg;
	uint32_t length   = cmd;
	scout_kernel_ctx_t ctx;
    scout_header_t header;
	int res;
	uint8_t * buffer = NULL, * origBuffer = NULL;

	SCOUT_LOG(KERN_INFO, "ioctl() was called with length = %d\n", length);

	memset(&ctx, 0, sizeof(scout_kernel_ctx_t));

    /* Fetch the instruction from the user */
	origBuffer = buffer = (uint8_t *)kmalloc(length, GFP_KERNEL);
	copy_from_user(buffer, p, length);

    /* Prepare the outgoing data streams */
	ctx.output = (uint8_t  * __user)((addr_t *)buffer)[0];
	ctx.stats  = (uint32_t * __user)((addr_t *)buffer)[1];
	buffer += sizeof(addr_t) * 2;
	length -= sizeof(addr_t) * 2;

    /* Set up the header */
    memcpy(&header, buffer, sizeof(header));
    buffer += sizeof(header);
    length -= sizeof(header);

	/* Call the generic API */
	res = handle_instruction(&ctx, &header, buffer);

	/* Free the allocated memory */
	kfree(origBuffer);

	return res;
}

/***************************/
/**  Driver Inits & fops  **/
/***************************/

static struct file_operations fops =
{
	.open           = dev_open,
	.unlocked_ioctl = scout_ioctl,
	.release        = dev_release,
};

static int __init scout_init(void)
{
    struct device* scoutDevice = NULL;

	majorNumber = register_chrdev(0, DEVICE_NAME, &fops);
	if (majorNumber < 0)
	{
		SCOUT_LOG(KERN_ALERT, "Failed to register the major number\n");
		return majorNumber;
	}

	scoutClass = class_create(THIS_MODULE, CLASS_NAME);
	if(IS_ERR(scoutClass))
	{
		unregister_chrdev(majorNumber, DEVICE_NAME);
		SCOUT_LOG(KERN_ALERT, "Failed to register the device class\n");
		return PTR_ERR(scoutClass);
	}

	scoutDevice = device_create(scoutClass, NULL, MKDEV(majorNumber, 0), NULL, DEVICE_NAME);
	if (IS_ERR(scoutDevice))
	{
		class_destroy(scoutClass);
		unregister_chrdev(majorNumber, DEVICE_NAME);
		SCOUT_LOG(KERN_ALERT, "Failed to create the device\n");
		return PTR_ERR(scoutDevice);
	}
	return 0;
}

static void __exit scout_exit(void)
{
	device_destroy(scoutClass, MKDEV(majorNumber, 0));
	class_unregister(scoutClass);
	class_destroy(scoutClass);
	unregister_chrdev(majorNumber, DEVICE_NAME);
}

static int dev_open(struct inode *inodep, struct file *filep)
{
	scout_open();
	return 0;
}

static int dev_release(struct inode *indoep, struct file *filep)
{
	return 0;
}

MODULE_AUTHOR("Eyal Itkin");
MODULE_DESCRIPTION("Scout based debug driver");
MODULE_LICENSE("GPL");

module_init(scout_init);
module_exit(scout_exit);
