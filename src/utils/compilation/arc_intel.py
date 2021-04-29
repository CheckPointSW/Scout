from target_arc import targetArc

class arcIntel(targetArc):
    def __init__(self, is_pic):
        super(arcIntel, self).__init__(is_pic)
        
    @staticmethod
    def name():
        """Get the architecture's name

        Return Value:
            String name for the architecture
        """
        return "Intel"
        
    # Overridden base function
    def setEndianness(self, is_little):
        if not is_32_bits:
            raise Exception("Intel doesn't support Big Endian :(")

    # Overridden base function
    def setBitness(self, is_32_bits):
        if not is_32_bits:
            return
        self.compile_flags += ('m32',)
        self.link_flags    += ('melf_i386',)