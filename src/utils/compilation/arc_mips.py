from target_arc import targetArc

class arcMips(targetArc):
    # Mips Toolchain
    mips_compiler_path  = '/usr/bin/mips-linux-gnu-gcc'
    mips_linker_path    = '/usr/bin/mips-linux-gnu-ld'
    mips_objcopy_path   = '/usr/bin/mips-linux-gnu-objcopy'
    mips_objcopy_flags  = ('--section-alignment 4',)
    
    mips_pic_compile_flags = ('fno-jump-tables', 'mno-shared', 'mplt')

    def __init__(self, is_pic):
        super(arcMips, self).__init__(is_pic)
        # Arc specific PIC flags
        if is_pic:
            self.compile_flags += mips_pic_compile_flags
            
    @staticmethod
    def name():
        """Get the architecture's name

        Return Value:
            String name for the architecture
        """
        return "Mips"

    # Overridden base function
    def setNotNative(self):
        self.setToolchain(mips_compiler_path, mips_linker_path, mips_objcopy_path, mips_objcopy_flags)
        
    # Overridden base function
    def setEndianness(self, is_little):
        if is_little:
            self.compile_flags += ('EL',)
            self.link_flags    += ('EL',)
        else:
            self.compile_flags += ('EB',)
            self.link_flags    += ('EB',)

    # Overridden base function
    def setBitness(self, is_32_bits):
        if not is_32_bits:
            raise NotImplementedError("Didn't yet implement the logic for 64 bits Mips")