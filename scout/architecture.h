#ifndef __SCOUT__ARCHITECTURE__H__
#define __SCOUT__ARCHITECTURE__H__

#include "flags.h"

#if defined(SCOUT_MODE_KERNEL) && !defined(SCOUT_PIC_CODE)
#include <linux/types.h>
#else
#include <stdint.h>
#endif /* SCOUT_MODE_KERNEL && !SCOUT_PIC_CODE */

/******************/
/**  Endianness  **/
/******************/

/* Sanity check */
#if defined(SCOUT_BIG_ENDIAN) && defined(SCOUT_LITTLE_ENDIAN)
    #error "Both big AND little endian are defined!"
#endif

/* Default values */
#if !defined(SCOUT_BIG_ENDIAN) && !defined(SCOUT_LITTLE_ENDIAN)
    #define SCOUT_LITTLE_ENDIAN
#endif

/***************/
/**  Bitness  **/
/***************/

/* Sanity check */
#if defined(SCOUT_BITS_32) && defined(SCOUT_BITS_64)
    #error "Both 32 AND 64 bits are defined!"
#endif

/* Default values */
#if !defined(SCOUT_BITS_32) && !defined(SCOUT_BITS_64)
    #define SCOUT_BITS_32
#endif

#ifdef SCOUT_BITS_32
typedef uint32_t addr_t;
#else
typedef uint64_t addr_t;
#endif /* SCOUT_BITS_32 */

/************************/
/**  CPU Architecture  **/
/************************/

/* Sanity check */
#undef SCOUT_ARCH
#if defined(SCOUT_ARCH_INTEL)
    #define SCOUT_ARCH
#endif
#if defined(SCOUT_ARCH_ARM)
    #if defined(SCOUT_ARCH)
        #error "Multiple CPU architecture are defined!"
    #else
        #define SCOUT_ARCH
    #endif
#endif
#if defined(SCOUT_ARCH_MIPS)
    #if defined(SCOUT_ARCH)
        #error "Multiple CPU architecture are defined!"
    #else
        #define SCOUT_ARCH
    #endif
#endif

#if defined(SCOUT_ARM_THUMB) && !defined(SCOUT_ARCH_ARM)
    #error "ARM Thumb-Mode must only be used when ARM CPU architecture is defined!"
#endif

/* Default values */
#if !defined(SCOUT_ARCH)
    #define SCOUT_ARCH_INTEL
#endif

/******************************/
/**  User Mode / Privileges  **/
/******************************/

/* Sanity check */
#if defined(SCOUT_MODE_USER) && defined(SCOUT_MODE_KERNEL)
    #error "Both user-mode AND kernel-mode are defined!"
#endif

/* Default values */
#if !defined(SCOUT_MODE_USER) && !defined(SCOUT_MODE_KERNEL)
    #define SCOUT_MODE_USER
#endif

/* Mainly used for readability */
#if defined(SCOUT_MODE_KERNEL)
	#define SCOUT_HIGH_PRIVILEGES
#endif

/***************************************/
/**  Excutable / Injected (PIC) Code  **/
/***************************************/

/* Mainly used for readability */
#if defined(SCOUT_PIC_CODE)
    #define SCOUT_ISOLATED_ENV
#endif

#endif // __SCOUT__ARCHITECTURE__H__