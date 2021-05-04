from .target_arc import targetArc

class arcMips(targetArc):
    """A class representing a Mips CPU architecture to which we will compile our binary.

    Attributes
    ----------
        (all inherited from the base class)
    """

    # Mips Toolchain
    mips_compiler_path  = '/usr/bin/mips-linux-gnu-gcc'
    mips_linker_path    = '/usr/bin/mips-linux-gnu-ld'
    mips_objcopy_path   = '/usr/bin/mips-linux-gnu-objcopy'
    mips_objcopy_flags  = ('--section-alignment 4',)

    mips_pic_compile_flags = ('fno-jump-tables', 'mno-shared', 'mplt')

    def __init__(self, is_pic):
        """Init the compilation configuration for the Mips architecture.

        Args:
            is_pic (bool): True iff a position-independent compilation
        """
        super(arcMips, self).__init__(is_pic)
        # Arc specific PIC flags
        if is_pic:
            self.compile_flags += self.mips_pic_compile_flags

    @staticmethod
    def name():
        """Get the architecture's name.

        Return Value:
            String name for the architecture
        """
        return "Mips"

    # Overridden base function
    def setNotNative(self):
        """Mark the compilation as using a toolchain and not the native compiler."""
        self.setToolchain(self.mips_compiler_path, self.mips_linker_path, self.mips_objcopy_path, self.mips_objcopy_flags)

    # Overridden base function
    def setEndianness(self, is_little):
        """Set the (little/big) endianness we are going to use.

        Args:
            is_little (bool): True iff compiling a Little Endian binary
        """
        if is_little:
            self.compile_flags += ('EL',)
            self.link_flags    += ('EL',)
        else:
            self.compile_flags += ('EB',)
            self.link_flags    += ('EB',)

    # Overridden base function
    def setBitness(self, is_32_bits):
        """Set the (32/64) bitness we are going to use.

        Args:
            is_32_bits (bool): True iff compiling a 32-bits binary
        """
        if not is_32_bits:
            raise NotImplementedError("Didn't yet implement the logic for 64 bits Mips")
