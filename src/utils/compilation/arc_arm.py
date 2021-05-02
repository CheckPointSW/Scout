from .target_arc import targetArc

class arcArm(targetArc):
    """A class representing an Arm CPU architecture to which we will compile our binary.

    Attributes
    ----------
        (all inherited from the base class)

    Notes
    -----
        Can be extended by the Arm-Thumb architecture class.
    """

    # Arm Toolchain
    arm_compiler_path = '/usr/bin/arm-none-eabi-gcc'
    arm_linker_path   = '/usr/bin/arm-none-eabi-ld'
    arm_objcopy_path  = '/usr/bin/arm-none-eabi-objcopy'
    arm_objcopy_flags = ('--section-alignment 4',)

    arm_pic_compile_flags = ('fno-jump-tables', 'mapcs-frame')

    def __init__(self, is_pic):
        """Init the compilation configuration for the Arm architecture.

        Args:
            is_pic (bool): True iff a position-independent compilation
        """
        super(arcArm, self).__init__(is_pic)
        # Arc specific PIC flags
        if is_pic:
            self.compile_flags += self.arm_pic_compile_flags

    @staticmethod
    def name():
        """Get the architecture's name.

        Return Value:
            String name for the architecture
        """
        return "Arm"

    # Overridden base function
    def setNotNative(self):
        """Mark the compilation as using a toolchain and not the native compiler."""
        self.setToolchain(self.arm_compiler_path, self.arm_linker_path, self.arm_objcopy_path, self.arm_objcopy_flags)

    # Overridden base function
    def setEndianness(self, is_little):
        """Set the (little/big) endianness we are going to use.

        Args:
            is_little (bool): True iff compiling a Little Endian binary
        """
        if is_little:
            self.compile_flags += ('mlittle-endian',)
            self.link_flags    += ('EL',)
        else:
            self.compile_flags += ('mbig-endian',)
            self.link_flags    += ('EB',)

    # Overridden base function
    def setBitness(self, is_32_bits):
        """Set the (32/64) bitness we are going to use.

        Args:
            is_32_bits (bool): True iff compiling a 32-bits binary
        """
        if not is_32_bits:
            raise NotImplementedError("Didn't yet implement the logic for 64 bits ARM")

class arcArmThumb(arcArm):
    """A class representing an Arm CPU architecture to which we will compile our Thumb binary.

    Attributes
    ----------
        (all inherited from the base class)
    """

    def __init__(self, is_pic):
        """Init the compilation configuration for the Arm-Thumb architecture.

        Args:
            is_pic (bool): True iff a position-independent compilation
        """
        super(arcArmThumb, self).__init__(is_pic)
        # Arc specific flags
        self.compile_flags += ('mthumb',)

    @staticmethod
    def name():
        """Get the architecture's name.

        Return Value:
            String name for the architecture
        """
        return "Arm-Thumb"

    # Overridden base function
    def setBitness(self, is_32_bits):
        """Set the (32/64) bitness we are going to use.

        Args:
            is_32_bits (bool): True iff compiling a 32-bits binary
        """
        if not is_32_bits:
            raise Exception("Not sure if ARM-Thumb even supports 64 bits")
