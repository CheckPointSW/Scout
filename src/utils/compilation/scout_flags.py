#############################
##  Static Configurations  ##
#############################

# flags files
FLAGS_FILE_NAME     = 'flags.h'

# configuration compile flags
flag_32_bit         = 'SCOUT_BITS_32'
flag_64_bit         = 'SCOUT_BITS_64'
flag_big_endian     = 'SCOUT_BIG_ENDIAN'
flag_little_endian  = 'SCOUT_LITTLE_ENDIAN'
flag_arc_intel      = 'SCOUT_ARCH_INTEL'
flag_arc_arm        = 'SCOUT_ARCH_ARM'
flag_arc_thumb      = 'SCOUT_ARM_THUMB'
flag_arc_mips       = 'SCOUT_ARCH_MIPS'
flag_mode_user      = 'SCOUT_MODE_USER'
flag_mode_kernel    = 'SCOUT_MODE_KERNEL'
flag_pic_code       = 'SCOUT_PIC_CODE'
flag_host_glibc     = 'SCOUT_HOST_GLIBC'
flag_host_uclibc    = 'SCOUT_HOST_UCLIBC'
flag_instructions   = 'SCOUT_INSTRUCTIONS'
flag_restore_flow   = 'SCOUT_RESTORE_FLOW'
flag_dynamic_buffers= 'SCOUT_DYNAMIC_BUFFERS'
flag_proxy          = 'SCOUT_PROXY'
flag_mmap           = 'SCOUT_MMAP'
flag_load_thumb     = 'SCOUT_LOADING_THUMB_CODE'
flag_loader         = 'SCOUT_LOADER'
flag_loader_client  = 'SCOUT_TCP_CLIENT'
flag_loader_server  = 'SCOUT_TCP_SERVER'
flag_loader_transmit= 'SCOUT_TCP_SEND'