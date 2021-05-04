from .target_arc import targetArc

class arcIntel(targetArc):
    """A class representing an Intel CPU architecture to which we will compile our binary.

    Attributes
    ----------
        (all inherited from the base class)
    """

    def __init__(self, is_pic):
        """Init the compilation configuration for Intel architecture.

        Args:
            is_pic (bool): True iff a position-independent compilation
        """
        super(arcIntel, self).__init__(is_pic)

    @staticmethod
    def name():
        """Get the architecture's name.

        Return Value:
            String name for the architecture
        """
        return "Intel"

    # Overridden base function
    def setEndianness(self, is_little):
        """Set the (little/big) endianness we are going to use.

        Args:
            is_little (bool): True iff compiling a Little Endian binary
        """
        if not is_little:
            raise Exception("Intel doesn't support Big Endian :(")

    # Overridden base function
    def setBitness(self, is_32_bits):
        """Set the (32/64) bitness we are going to use.

        Args:
            is_32_bits (bool): True iff compiling a 32-bits binary
        """
        if not is_32_bits:
            return
        self.compile_flags += ('m32',)
        self.link_flags    += ('melf_i386',)
