class targetArc:
    native_compiler_path = 'gcc'
    native_linker_path   = 'ld'
    native_objcopy_path  = 'objcopy'
    native_objcopy_flags = ()

    base_compile_flags            = ('fno-builtin', 'Wno-int-to-pointer-cast', 'Wno-pointer-to-int-cast')
    base_executable_compile_flags = ('O2',)
    base_pic_compile_flags        = ('Os', 'nostdlib', 'fno-toplevel-reorder')
    base_link_flags               = ()
    
    def __init__(self, is_pic):
        self.compiler_path = native_compiler_path
        self.linker_path   = native_linker_path
        self.objcopy_path  = native_objcopy_path
        self.objcopy_flags = list(native_objcopy_flags)
        
        self.compile_flags = list(base_compile_flags)
        self.link_flags    = list(base_link_flags)
        
        self.compile_flags += base_pic_compile_flags if is_pic else base_executable_compile_flags

    def setToolchain(self, compiler_path, linker_path, objcopy_path, objcopy_flags):
        self.compiler_path = compiler_path
        self.linker_path   = linker_path
        self.objcopy_path  = objcopy_path
        self.objcopy_flags = [] + objcopy_flags
        
    def setNotNative(self):
        raise NotImplementedError("Subclasses should implement this!")
        
    def setEndianness(self, is_little):
        raise NotImplementedError("Subclasses should implement this!")
        
    def setBitness(self, is_32_bits):
        raise NotImplementedError("Subclasses should implement this!")
        
    def prepareFlags(self):
        compile_flags = ' '.join(['-' + x for x in self.compile_flags])
        link_flags    = ' '.join(['-' + x for x in self.link_flags])
        return compile_flags, link_flags