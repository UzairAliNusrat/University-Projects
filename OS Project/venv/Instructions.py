



#This Instruction class is where all those instructions are implemented that require access to registers.
#We have created a register object from the register class to have access of of each register.
# Throughout the Instruction class, The instructions move/add/subtract etc the contents of one register are moved to the other.
#This is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register.

#In the following instructions, functions try excepting blocks to catch the overflow error and then finally print all the contents of the block of General registers.

class instruction():
#this class is where all those instructions are implemented that require access to registers. we have created a register object
#from the register class to have access of of each register




#in this Move function contents of one register are moved to the other.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register
    def MOV(self, hexCode1, hexCode2, process):

        index1 = process.registers.hexArr.index(hexCode1)
        index2 = process.registers.hexArr.index(hexCode2)
        process.registers.registerArr[index1] = process.registers.registerArr[index2]
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big", signed=True))

#in this Add function contents of one register are added to the other and stored back in the register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def ADD(self,hexCode1,hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            result = int.from_bytes(process.registerArr[index1], "big", signed=True) + int.from_bytes(
                process.registers.registerArr[index2], "big", signed=True)
            process.registers.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1

        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow,signbit,zerobit

#in this Subtract function contents of one register are subtracted from the other and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def SUB(self, hexCode1, hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            num1 = int.from_bytes(process.registers.registerArr[index1], "big", signed=True)
            num2 = int.from_bytes(process.registers.registerArr[index2], "big", signed=True)
            result = num1 - num2
            self.reg.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow,signbit,zerobit

##in this Multiply function contents of one register are multiplied with the other and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def MUL(self,hexCode1,hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            result = int.from_bytes(process.registers.registerArr[index1], "big", signed=True) * int.from_bytes(
                process.registers.registerArr[index2], "big", signed=True)
            process.registers.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))

            return overflow,signbit,zerobit

#in this Divide function contents of one register are divided with the other and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def DIV(self,hexCode1,hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            result = int.from_bytes(process.registers.registerArr[index1], "big", signed=True) // int.from_bytes(
                process.registers.registerArr[index2], "big", signed=True)
            process.registers.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow,signbit,zerobit

#in this AND function contents of one register are AND'ed with the other and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def AND(self,hexCode1,hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            result = int.from_bytes(process.registers.registerArr[index1], "big", signed=True) and int.from_bytes(process.registers.registerArr[index2], "big", signed=True)
            process.registers.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this OR function contents of one register are OR'ed with the other and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def OR(self,hexCode1,hexCode2, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index1 = process.registers.hexArr.index(hexCode1)
            index2 = process.registers.hexArr.index(hexCode2)
            result = int.from_bytes(process.registers.registerArr[index1], "big", signed=True) or int.from_bytes(process.registers.registerArr[index2], "big",signed=True)
            process.registers.registerArr[index1] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this Move Immidiate function, an immidiate number is moved to a register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register
    def MOVI(self,hex1, num, process):
        index = process.registers.hexArr.index(hex1)
        print(index)
        process.registers.registerArr[index] = num
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big",signed=True))

#in this ADD Immidiate function, an immidiate number is added to the contents of a register and result is put in the register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def ADDI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            result = int.from_bytes(process.registers.registerArr[index], "big", signed=True) + int.from_bytes(num, "big",signed=True)
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this Subtract Immidiate function, an immidiate number is subtracted from the contents of a register and result is put in the register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def SUBI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            num1 = int.from_bytes(process.registers.registerArr[index], "big", signed=True)
            num2 = int.from_bytes(num, "big", signed=True)
            result = num1 - num2
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this Multiply Immidiate function, an immidiate number is Multiplied with the contents of a register and result is put in the register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def MULI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            result = int.from_bytes(process.registers.registerArr[index], "big", signed=True) * int.from_bytes(num, "big",signed=True)
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this Divide Immidiate function, an immidiate number and the contents of a register are divided and result is put in the register.this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def DIVI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            result = int.from_bytes(process.registers.registerArr[index], "big", signed=True) // int.from_bytes(num, "big",signed=True)
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this AND Immidiate function contents of one register are AND'ed with an immidiate number and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def ANDI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            result = int.from_bytes(process.registers.registerArr[index], "big", signed=True) and int.from_bytes(num, "big", signed=True)
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this OR Immidiate function contents of one register are OR'ed with an immidiate number and stored back in the register. this is done by first finding out the index
#of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def ORI(self,hex1, num, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            index = process.registers.hexArr.index(hex1)
            result = int.from_bytes(process.registers.registerArr[index], "big", signed=True) or int.from_bytes(num, "big", signed=True)
            process.registers.registerArr[index] = (result).to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit

#in this MOVL function, an immidiate is stored inside a register.this is done by first finding out the index of the register hexcode in the hexArray inside the register class
#and then inputting that index in the register array of the
#register class to get the corresponding register.
    def MOVL(self, hex1, num, process):
        index = process.registers.hexArr.index(hex1)
        process.registers.registerArr[index] = num
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big", signed=True))








#in this MOVS function, the contents of register are read and then returned back to the main class where the instruction was called, the contents will then be stored inside the memory array at a specific index.
# this is done by first finding out the index of the register hexcode in the hexArray inside the register class
#and then inputting that index in the register array of the
#register class to get the corresponding register.
    def MOVS(self,hex1, process):
        index = process.registers.hexArr.index(hex1)
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big",signed=True))
        return process.registers.registerArr[index]

#in this Shift Left function, contents of a register are shifted to the left by one bit and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def SHL(self,hex1, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            carrybit = 0
            index = process.registers.hexArr.index(hex1)
            temp = int.from_bytes(process.registers.registerArr[index], "big", signed=True)
            if temp < 0:
                carrybit = 1
            result = temp << 1
            process.registers.registerArr[index] = result.to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit, carrybit

#in this Shift Right function, contents of a register are shifted to the Right by one bit and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def SHR(self,hex1, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            carrybit = 0
            index = process.registers.hexArr.index(hex1)
            temp = int.from_bytes(process.registers.registerArr[index], "big", signed=True)
            if temp < 0:
                carrybit = 1
            result = temp >> 1
            process.registers.registerArr[index] = result.to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit, carrybit

#in this Rotate Left function, contents of a register are rotated to the left by one bit and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def RTL(self,hex1, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            carrybit = 0
            index = process.registers.hexArr.index(hex1)
            temp = int.from_bytes(process.registers.registerArr[index], "big", signed=True)
            binary = format(temp, "b")
            if temp < 0:
                carrybit = 1
            temp = temp << 1
            bina = format(temp, "b")
            binary1 = bina[1:len(bina) - 1] + binary[0:1]
            result = int(binary1, 2)
            process.registers.registerArr[index] = result.to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit, carrybit

#in this Rotate Right function, contents of a register are rotated to the Right by one bit and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register. all the code is inside try except blocks to catch the overflow error and then
#in the finally block all contents of the general registers are printed
    def RTR(self,hex1, process):
        try:
            overflow = 0
            zerobit = 0
            signbit = 0
            carrybit = 0
            index = process.registers.hexArr.index(hex1)
            temp = int.from_bytes(process.registers.registerArr[index], "big", signed=True)
            if temp < 0:
                carrybit = 1
            binary = format(temp, "b")
            temp = temp >> 1
            bina = binary[len(binary) - 1:len(binary)] + format(temp, "b")
            result = int(bina, 2)
            process.registers.registerArr[index] = result.to_bytes(2, "big", signed=True)
            if result == 0:
                zerobit = 1
            if result < 0:
                signbit = 1
        except OverflowError:
            print("overflow occurred")
            overflow = 1
        finally:
            for num in process.registers.registerArr:
                print(int.from_bytes(num, "big", signed=True))
            return overflow, signbit, zerobit, carrybit

#in this Increment function, the contents of a register are incrmemented by one and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register.
    def INC(self,hex1, process):
        index = process.registers.hexArr.index(hex1)
        temp = int.from_bytes(process.registers.registerArr[index], "big",signed=True)
        temp = temp + 1
        process.registers.registerArr[index] = temp.to_bytes(2,"big",signed=True)
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big",signed=True))

#in this Deccrement function, the contents of a register are Decrmemented by one and stored back in the register.
#this is done by first finding out the index of the register hexcode in the hexArray inside the register class and then inputting that index in the register array of the
#register class to get the corresponding register.
    def DEC(self,hex1, process):
        index = process.registers.hexArr.index(hex1)
        temp = int.from_bytes(process.registers.registerArr[index], "big",signed=True)
        temp = temp - 1
        process.registers.registerArr[index] = temp.to_bytes(2,"big",signed=True)
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big",signed=True))

    def PUSH(self,hex1, process):
        index = process.registers.hexArr.index(hex1)
        temp = int.from_bytes(process.registers.registerArr[index], "big", signed=False)
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big", signed=True))
        return temp

    def POP(self,hex1, stackVal, process):
        index = process.registers.hexArr.index(hex1)
        process.registers.registerArr[index] = stackVal
        for num in process.registers.registerArr:
            print(int.from_bytes(num, "big", signed=True))


