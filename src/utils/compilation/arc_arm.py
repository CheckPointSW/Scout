from target_arc import targetArc

class arcArm(targetArc):
    # Arm Toolchain
    arm_compiler_path = '/usr/bin/arm-none-eabi-gcc'
    arm_linker_path   = '/usr/bin/arm-none-eabi-ld'
    arm_objcopy_path  = '/usr/bin/arm-none-eabi-objcopy'
    arm_objcopy_flags = ('--section-alignment 4',)
    
    arm_pic_compile_flags = ('fno-jump-tables', 'mapcs-frame')

    def __init__(self, is_pic):
        super(arcArm, self).__init__(is_pic)
        # Arc specific PIC flags
        if is_pic:
            self.compile_flags += arm_pic_compile_flags

    @staticmethod
    def name():
        """Get the architecture's name

        Return Value:
            String name for the architecture
        """
        return "Arm"
    
    # Overridden base function
    def setNotNative(self):
        self.setToolchain(arm_compiler_path, arm_linker_path, arm_objcopy_path, arm_objcopy_flags)

    # Overridden base function
    def setEndianness(self, is_little):
        if is_little:
            self.compile_flags += ('mlittle-endian',)
            self.link_flags    += ('EL',)
        else:
            self.compile_flags += ('mbig-endian',)
            self.link_flags    += ('EB',)
    
    # Overridden base function
    def setBitness(self, is_32_bits):
        if not is_32_bits:
            raise NotImplementedError("Didn't yet implement the logic for 64 bits ARM")
            
class arcArmThumb(arcArm):
    def __init__(self, is_pic):
        super(arcArmThumb, self).__init__(is_pic)
        # Arc specific flags
        self.compile_flags += ('mthumb',)

    @staticmethod
    def name():
        """Get the architecture's name

        Return Value:
            String name for the architecture
        """
        return "Arm-Thumb"

    # Overridden base function
    def setBitness(self, is_32_bits):
        if not is_32_bits:
            raise Exception("Not sure if ARM-Thumb even supports 64 bits")