#ifndef __SCOUT__ARCHITECTURE__H__
#define __SCOUT__ARCHITECTURE__H__

#include "flags.h"

#if defined(SCOUT_MODE_KERNEL) && defined(SCOUT_PC_ENV)
#include <linux/types.h>
#else
#include <stdint.h>
#endif /* SCOUT_MODE_KERNEL && SCOUT_PC_ENV */

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
#if defined(SCOUT_ARCH_INTEL) && defined(SCOUT_ARCH_ARM)
    #error "Both Intel CPU architecture AND ARM CPU architecture are defined!"
#endif

/* Default values */
#if !defined(SCOUT_ARCH_INTEL) && !defined(SCOUT_ARCH_ARM)
    #define SCOUT_ARCH_INTEL
#endif

/******************/
/**  User Level  **/
/******************/

/* Sanity check */
#if defined(SCOUT_MODE_USER) && defined(SCOUT_MODE_KERNEL)
    #error "Both user-mode AND kernel-mode are defined!"
#endif

/* Default values */
#if !defined(SCOUT_MODE_USER) && !defined(SCOUT_MODE_KERNEL)
    #define SCOUT_MODE_USER
#endif

/****************/
/**  Embedded  **/
/****************/

/* Sanity check */
#if defined(SCOUT_EMBEDDED_ENV) && defined(SCOUT_PC_ENV)
    #error "Both embedded environment AND PC environment are defined!"
#endif

/* Default values */
#if !defined(SCOUT_EMBEDDED_ENV) && !defined(SCOUT_PC_ENV)
    #define SCOUT_PC_ENV
#endif

/****************/
/**  PIC Code  **/
/****************/

/* Sanity check */
#if defined(SCOUT_PIC_CODE) && !defined(SCOUT_EMBEDDED_ENV)
    #error "PIC code can only be used in an embedded environment!"
#endif

/* Sanity check */
#if !defined(SCOUT_PIC_CODE) && defined(SCOUT_EMBEDDED_ENV)
    #error "For now, embedded environment must be used only with PIC code"
#endif

#endif // __SCOUT__ARCHITECTURE__H__
