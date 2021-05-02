#include "scout_kernel_instructions.h"
#include "scout/pack.h"
#include <linux/random.h>
#include <asm/io.h>

/* Symbol of the leaked function */
extern void add_input_randomness(unsigned int type, unsigned int code, unsigned int value);

void register_specific_instructions(void)
{
    register_instruction(KERNEL_INST_PHY_READ,  INSTR_PHY_READ_MIN_SIZE,  INSTR_PHY_READ_MAX_SIZE,  INSTR_PHY_READ_HANDLER);
    register_instruction(KERNEL_INST_PHY_WRITE, INSTR_PHY_WRITE_MIN_SIZE, INSTR_PHY_WRITE_MAX_SIZE, INSTR_PHY_WRITE_HANDLER);
    register_instruction(KERNEL_INST_LEAK_ADDR, INSTR_LEAK_ADDR_MIN_SIZE, INSTR_LEAK_ADDR_MAX_SIZE, INSTR_LEAK_ADDR_HANDLER);
}

int instruction_phy_read(void * c, uint8_t * instruction, uint32_t length)
{
    scout_kernel_ctx_t * ctx = (scout_kernel_ctx_t *)c;
    addr_t src;
    uint8_t * readHead = instruction;
    /**
     * In recent kernels there is a check on direct kernel<->user copy operations
     * so we use an intermediate buffer to bypass them.
     */
    uint8_t local_buffer[MAX_IO_REQUEST];

    src    = unpack_addr(&readHead);
    length = unpack_uint32(&readHead);

    if(length > MAX_IO_REQUEST)
    {
        return STATUS_ILLEGAL_LENGTH;
    }
    memcpy(local_buffer, phys_to_virt(src), length);

    write_output(ctx, local_buffer, length);

    return STATUS_OK;
}

int instruction_phy_write(void * c, uint8_t * instruction, uint32_t length)
{
    addr_t dest;
    uint8_t * readHead = instruction;

    (void)c;

    dest = unpack_addr(&readHead);
    length -= sizeof(addr_t);

    memcpy(phys_to_virt(dest), readHead, length);

    return STATUS_OK;
}

int instruction_leak_addr(void * c, uint8_t * instruction, uint32_t length)
{
    scout_kernel_ctx_t * ctx = (scout_kernel_ctx_t *)c;
    uint8_t * ptr = (uint8_t*)add_input_randomness;

    (void)instruction;
    (void)length;

    /* Leaking the address of the pre-defined function: add_input_randomness */
    write_output(ctx, &ptr, sizeof(addr_t));
    ptr = (void *)virt_to_phys(add_input_randomness);
    write_output(ctx, &ptr, sizeof(addr_t));

    printk(KERN_NOTICE "SCOUT-KERNEL: virt addres is 0x%p, phys is 0x%p\n", add_input_randomness, (void *)virt_to_phys(add_input_randomness));

    return STATUS_OK;
}
