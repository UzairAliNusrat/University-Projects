from Instructions import instruction
from PCB import pcb



    #This Virtual Machine class, acts like Computer Operating Ssystem.
    # This executes all the instructions of the 'Instructions' class and use the 'Register' class for data retrieval, storage and access.
class VM():




    # This is a Dictionary declared with hexadecimal values and their corresponding opcodes.
    a = {"16": "MOV", "17": "ADD", "18": "SUB", "19": "MUL", "1A": "DIV", "1B": "AND", "1C": "OR", "30": "MOVI",
         "31": "ADDI", "32": "SUBI", "33": "MULI", "34": "DIVI", "35": "ANDI", "36": "ORI", "37": "BZ", "38": "BNZ",
         "39": "BC", "3A": "BS", "3B": "JMP", "3C": "CALL", "3D": "ACT", "51": "MOVL",
         "52": "MOVS", "71": "SHL", "72": "SHR", "73": "RTL", "74": "RTR", "75": "INC",
         "76": "DEC", "77": "PUSH", "78": "POP", "F1": "RETURN", "F2": "NOOP", "F3": "END"}

    # This is the Flag Register
    flagReg = [0] * 16

     #In this portion of the code, CPU Scheduling Algorithms have been implemented. The code is written in a way that it (CPU) checks the PCB data and
    #ensures there is no error. Finally it takes that PCB to the ready queue where it is given the access to running queue when an old process has been executed.
    #Moreover, while the process is getting the access to the running queue, for it being excecuted it is given the required amount of memory.
    #The memory management implementation has been done using the concept of 'Fragmentation' and 'Paging'.

    def run(self):

        temparr = [[0 for i in range(128)] for j in range(512)]
        byte_arrayMem = temparr
        # A Priority Queue is made to store and manage processes with a given priority.

        Q1 = []
        Q2 = []
        file = open('/home/uzair/Downloads/processes.txt', 'rb')
        array = []
        j = 0
        row = 0
        col = 0
        instruc = instruction()
        for path in file:

            fileA = open(path[0:len(path) - 1], 'rb')
            while True:
                temp = fileA.read(1)
                if not temp:
                    break
                array.append(ord(temp))
            priority = array[0]

            processID = self.conversion(hex(array[1])[2:], hex(array[2])[2:])
            filename = path[0:len(path) - 1][22:]

            dataSize = self.conversion(hex(array[3])[2:], hex(array[4])[2:])
            codeSize = len(array) - dataSize - 8
            processSize = len(array) + 50

            process = pcb(processID, priority, filename, processSize, codeSize, dataSize)

            if priority >= 0 and priority <= 15:
                Q1.append((process.process_priority, process))

            if priority > 15 and priority <= 31:
                Q2.append(process)



            process.codebaseRowCol = (row,col)
            for i in range(8 + dataSize, len(array), 1):
                if col > 127:
                    process.pageTable.append(row)
                    row = row + 1
                    col = 0
                temparr[row][col] = array[i]
                col = col + 1
            process.codelimitRowCol = (row,col - 1)

            process.dataBaseRowCol = (row, col)
            for i in range(8, 8 + dataSize, 1):
                if col > 127:
                    process.pageTable.append(row)
                    row = row + 1
                    col = 0
                temparr[row][col] = array[i]
                col = col + 1

            process.dataLimitRowCol = (row, col - 1)

            process.stackStartRowCol = (row, col)


            for i in range(50):
                if col > 127:
                    process.pageTable.append(row)
                    row = row + 1
                    col = 0
                temparr[row][col] = 0
                col = col + 1
            process.stackEndRowCol = (row, col - 1)

            if col <= 127:
                process.pageTable.append(row)



            print(process.pageTable)
            row = row + 1
            col = 0


            array.clear()
        file.close()
        fileA.close()

        Q1.sort(key=lambda a: a[0])

        print(Q1)



        #for row in range(0, len(temparr), 1):
         #   print(temparr[row])


        #After the process has been loaded into the Running queue, the instructions are read and the process is given its required amount of memory to use written in its PCB.



        #input file is opened
        #file = open('/home/uzair/Downloads/p1.txt', 'r')

        # The file is then read.
        # The numbers in the file are read as Strings and converted to Int and stored in the temp array.

        # for number in file:
        # temparr.append(int(number))
        # self.codecounter = self.codecounter + 1
        # file.close

        # Now this temp arrar is converted to a byte array which is the memory array for this Virtual Machine.
        for row in range(len(temparr)):
            for col in range(len(temparr[row])):
                byte_arrayMem[row][col] = temparr[row][col].to_bytes(2,"big", signed=False)

        for row in range(len(byte_arrayMem)):
            print(byte_arrayMem[row])



        # Then the loop gets runned until every instruction in the memory array is executed.
        while len(Q1) != 0 or len(Q2) != 0:
            # Number is read from memory and converted to hex through a function that we have made.
            # This hex is put into the dictionary to get its corresponding opcode.
            if len(Q1) != 0:
                proc = Q1.pop(0)[1]

                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                programCounter = proc.codebaseRowCol[1]
                index = startRow
                stackindex = proc.stackEndRowCol[1]
                while index <= endRow:

                    hexa = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter], "big", signed=False))
                    print(self.a.get(hexa))

                    if self.a.get(hexa) == None:
                        print("Syntax Error")
                        break
                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ADDI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.SUBI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.MULI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.DIVI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ANDI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ORI(hex1,
                                                                                        sum.to_bytes(2, "big",
                                                                                                     signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        instruc.MOVL(hex1, byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.SHL(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.SHR(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.RTL(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.RTR(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = instruc.PUSH(hex1, proc)
                        proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            instruc.POP(hex1, val, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # this instruction does nothing and program counter moves to the next instruction
                    elif self.a.get(hexa) == "NOOP":
                        programCounter = programCounter + 1
                        print(self.flagReg)

                    # this instruction ends the entire virtual machine program
                    elif self.a.get(hexa) == "END":
                        print(self.flagReg)
                        print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                        break

                    if index < endRow and programCounter > 127:
                        index = index + 1
                        programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        index = index + 1


                print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")


            if len(Q1) == 0 and len(Q2) != 0:
                proc = Q2.pop(0)
                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                programCounter = proc.codebaseRowCol[1]
                index = startRow

                if proc.stackindexCol == -1:
                    stackindex = proc.stackEndRowCol[1]
                else:
                    stackindex = proc.stackindexCol

                timetaken = 0
                timeSlice = 8



                while index <= endRow:
                    hexa = self.int_to_hex(int.from_bytes(byte_arrayMem[index][programCounter], "big", signed=False))
                    print(self.a.get(hexa))
                    if self.a.get(hexa) == None:
                        print("Syntax Error")
                        print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                        break
                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)
                        instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ADDI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.SUBI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.MULI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.DIVI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ANDI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = instruc.ORI(hex1,
                                                                                        sum.to_bytes(2, "big",
                                                                                                     signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                               "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                               "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                               "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                               "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=False))
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=False) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=False)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        instruc.MOVL(hex1, byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(byte_arrayMem[index][programCounter + 3],
                                                                           "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.SHL(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.SHR(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.RTL(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = instruc.RTR(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = instruc.PUSH(hex1, proc)
                        if proc.stack.empty() == False:
                            proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",signed=False)
                        else:
                            if stackindex != -1:
                                byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big",signed=False)
                            else:
                                stackindex = 127
                                byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                   signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(
                            int.from_bytes(byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            instruc.POP(hex1, val, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # this instruction does nothing and program counter moves to the next instruction
                    elif self.a.get(hexa) == "NOOP":
                        programCounter = programCounter + 1
                        print(self.flagReg)

                    # this instruction ends the entire virtual machine program
                    elif self.a.get(hexa) == "END":
                        print(self.flagReg)
                        print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                        break



                    if index < endRow and programCounter > 127:
                        index = index + 1
                        programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                        index = index + 1

                    if timetaken == timeSlice and index <= endRow:
                        proc.codebaseRowCol= (index, programCounter)
                        proc.stackindexCol = stackindex
                        Q2.append(proc)
                        break
                    else:
                        timetaken = timetaken + 2


        print(len(Q1))
        print(len(Q2))


















    def conversion(self, temp1, temp2):
        if len(temp1) == 1:
            temp1 = "0" + temp1
        if len(temp2) == 1:
            temp2 = "0" + temp2
        return int(temp1 + temp2, 16)

    #method to convert integer to hexadecimal
    def int_to_hex(self,temp):
        hex = ""
        while (temp >= 0):
            remainder = temp % 16
            temp = temp // 16
            if remainder > 9:
                if remainder == 10:
                    hex = "A" + hex
                elif remainder == 11:
                    hex = "B" + hex
                elif remainder == 12:
                    hex = "C" + hex
                elif remainder == 13:
                    hex = "D" + hex
                elif remainder == 14:
                    hex = "E" + hex
                elif remainder == 15:
                    hex = "F" + hex
            else:
                hex = str(remainder) + hex

            if temp < 16:
                if temp > 9:
                    if temp == 10:
                        hex = "A" + hex
                    if temp == 11:
                        hex = "B" + hex
                    if temp == 12:
                        hex = "C" + hex
                    if temp == 13:
                        hex = "D" + hex
                    if temp == 14:
                        hex = "E" + hex
                    if temp == 15:
                        hex = "F" + hex
                else:
                    hex = str(temp) + hex
                temp = -1
        return hex




#Virtual machine object created and run through its run method.

phase1 = VM()
phase1.run()