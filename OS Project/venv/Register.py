class register:

    R0 = 0
    R1 = 0
    R2 = 0
    R3 = 0
    R4 = 0
    R5 = 0
    R6 = 0
    R7 = 0
    R8 = 0
    R9 = 0
    R10 = 0
    R11 = 0
    R12 = 0
    R13 = 0
    R14 = 0
    R15 = 0

    #the above general register int variables are converted to bytes of size two and stored in an array and throughout this
    #virtual machine program, these general registers are referred through this array. the above int registers are just variables
    #so that they could be converted to bytes in this array. each index of this array represents a general register
    #of byte size 2 which allows signed values
    registerArr = [R0.to_bytes(2, "big", signed = True), R1.to_bytes(2, "big", signed = True), R2.to_bytes(2, "big", signed = True),
                   R3.to_bytes(2, "big", signed = True), R4.to_bytes(2, "big", signed = True), R5.to_bytes(2, "big", signed = True),
                   R6.to_bytes(2, "big", signed = True), R7.to_bytes(2, "big", signed = True), R8.to_bytes(2, "big", signed = True),
                   R9.to_bytes(2, "big", signed = True), R10.to_bytes(2, "big", signed = True), R11.to_bytes(2, "big", signed = True),
                   R12.to_bytes(2, "big", signed = True), R13.to_bytes(2, "big", signed = True), R14.to_bytes(2, "big", signed = True),
                   R15.to_bytes(2, "big", signed = True)]

    #this array contains the hex codes for each register, so the hex code at first index of this array, corresponds
    #to the register at the first index of registerArr and so on. so when we read the hex code for a register from the memory
    # we can check for the index of that hex code in this array(hexArr) so that we know exactly which register is to be used in registerArr
    # by getting the register at that index that we found from this hexArr
    hexArr = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F"]






