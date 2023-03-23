
#By Uzair Ali Nusrat and Amanullah Faisal

from Instructions import instruction
from PCB import pcb
#from commands import commands



    #This Virtual Machine class, acts like Computer Operating Ssystem.
    # This executes all the instructions of the 'Instructions' class and use the 'Register' class for data retrieval, storage and access.
class VM():



    # This is a Dictionary declared with hexadecimal values and their corresponding opcodes.
    a = {"16": "MOV", "17": "ADD", "18": "SUB", "19": "MUL", "1A": "DIV", "1B": "AND", "1C": "OR", "30": "MOVI",
         "31": "ADDI", "32": "SUBI", "33": "MULI", "34": "DIVI", "35": "ANDI", "36": "ORI", "37": "BZ", "38": "BNZ",
         "39": "BC", "3A": "BS", "3B": "JMP", "3C": "CALL", "3D": "ACT", "51": "MOVL",
         "52": "MOVS", "71": "SHL", "72": "SHR", "73": "RTL", "74": "RTR", "75": "INC",
         "76": "DEC", "77": "PUSH", "78": "POP", "F1": "RETURN", "F2": "NOOP", "F3": "END"}

    frameTable = [False] * 512

    # This is the Flag Register
    flagReg = [0] * 16



     #In this portion of the code, CPU Scheduling Algorithms have been implemented. The code is written in a way that it (CPU) checks the PCB data and
    #ensures there is no error. Finally it takes that PCB to the ready queue where it is given the access to running queue when an old process has been executed.
    #Moreover, while the process is getting the access to the running queue, for it being excecuted it is given the required amount of memory.
    #The memory management implementation has been done using the concept of 'Fragmentation' and 'Paging'.

    temparr = [[0 for i in range(128)] for j in range(512)]
    byte_arrayMem = temparr


    for row in range(len(temparr)):
        for col in range(len(temparr[row])):
            byte_arrayMem[row][col] = temparr[row][col].to_bytes(2, "big", signed=False)


    array = []

    Q1 = []
    Q2 = []
    blocked = []
    row = 0
    col = 0

    instruc = instruction()
    last_executed = None

    def load(self, filename):
        file = open('/home/uzair/Downloads/processes.txt', 'r')
        pathA = ""
        found = False
        for path in file:
            fileName = str(path[:len(path) - 1][22:])
            if fileName == filename:
                fileA = open(path[0:len(path) - 1], 'rb')
                pathA = path
                found = True
                while True:
                    temp = fileA.read(1)
                    if not temp:
                        break
                    self.array.append(ord(temp))
                if found:
                    fileA.close()
                    break
        file.close()
        priority = self.array[0]

        processID = self.conversion(hex(self.array[1])[2:], hex(self.array[2])[2:])
        filename = pathA[0:len(pathA) - 1][22:]

        dataSize = self.conversion(hex(self.array[3])[2:], hex(self.array[4])[2:])
        codeSize = len(self.array) - dataSize - 8
        processSize = len(self.array) + 50

        process = pcb(processID, priority, filename, processSize, codeSize, dataSize)

        if priority >= 0 and priority <= 15:
            self.Q1.append((process.process_priority, process))

        if priority > 15 and priority <= 31:
            self.Q2.append(process)

        process.codebaseRowCol = (self.row, self.col)
        nextrow = True
        for i in range(8 + dataSize, len(self.array), 1):
            if self.col > 127:
                nextrow = True
                self.row = self.row + 1
                self.col = 0
            self.byte_arrayMem[self.row][self.col] = (int(self.array[i])).to_bytes(2,"big",signed=False)
            self.col = self.col + 1
            if nextrow:
                process.pageTable.append(self.row)
                nextrow = False
            self.frameTable[self.row] = True
        process.codelimitRowCol = (self.row, self.col - 1)

        process.dataBaseRowCol = (self.row, self.col)
        for i in range(8, 8 + dataSize, 1):
            if self.col > 127:
                nextrow = True
                self.row = self.row + 1
                self.col = 0
            self.byte_arrayMem[self.row][self.col] = (int(self.array[i])).to_bytes(2,"big",signed=False)
            self.col = self.col + 1
            if nextrow:
                process.pageTable.append(self.row)
                nextrow = False
            self.frameTable[self.row] = True

        process.dataLimitRowCol = (self.row, self.col - 1)

        process.stackStartRowCol = (self.row, self.col)

        for i in range(50):
            if self.col > 127:
                nextrow = True
                self.row = self.row + 1
                self.col = 0
            self.byte_arrayMem[self.row][self.col] = (0).to_bytes(2,"big",signed=False)
            self.col = self.col + 1
            if nextrow:
                process.pageTable.append(self.row)
                nextrow = False
            self.frameTable[self.row] = True
        process.stackEndRowCol = (self.row, self.col - 1)




        self.row = self.row + 1
        self.col = 0

        self.array.clear()
        self.Q1.sort(key=lambda a: a[0])


        print("process " + str(process.process_ID) + " loaded successfully!")

    def run_p(self, process_ID):
        for i in range(len(self.Q1)):
            proc = self.Q1.pop(i)[1]
            if str(proc.process_ID) == str(process_ID):
                self.Q1.insert(i, (proc.process_priority, proc))
                proc = self.Q1.pop(i)[1]

                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                programCounter = proc.codebaseRowCol[1]
                index = startRow
                stackindex = proc.stackEndRowCol[1]
                while index <= endRow:

                    hexa = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))
                    print(self.a.get(hexa))

                    if self.a.get(hexa) == None:
                        print("Syntax Error")
                        break
                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                             sum.to_bytes(2, "big",
                                                                                                          signed=True),
                                                                                             proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                 "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                   "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][self.programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.PUSH(hex1, proc)
                        proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                        signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            self.instruc.POP(hex1, val, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # this instruction does nothing and program counter moves to the next instruction
                    elif self.a.get(hexa) == "NOOP":
                        programCounter = programCounter + 1
                        print(self.flagReg)

                    # this instruction ends the entire virtual machine program
                    elif self.a.get(hexa) == "END":
                        print(self.flagReg)
                        break

                    if index < endRow and programCounter > 127:
                        index = index + 1
                        self.programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        index = index + 1


                self.last_executed = proc
                proc.terminated = True
                print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                self.kill_p(proc.process_ID)
                break

            else:
                self.Q1.insert(i, (proc.process_priority, proc))


        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if str(proc.process_ID) == str(process_ID):
                self.Q2.insert(i, proc)
                proc = self.Q2.pop(0)
                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                programCounter = proc.codebaseRowCol[1]
                index = startRow

                if proc.stackindexCol == -1:
                    stackindex = proc.stackEndRowCol[1]
                else:
                    stackindex = proc.stackindexCol


                while index <= endRow:
                    hexa = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))
                    print(self.a.get(hexa))
                    if self.a.get(hexa) == None:
                        print("Syntax Error")
                        print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                        break
                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                             sum.to_bytes(2, "big",
                                                                                                          signed=True),
                                                                                             proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)

                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                 "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                   "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)

                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=False))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=False) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=False)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)

                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.PUSH(hex1, proc)
                        if proc.stack.empty() == False:
                            proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                    signed=False)
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                      signed=False)
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                        signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            self.instruc.POP(hex1, val, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)

                    # this instruction does nothing and program counter moves to the next instruction
                    elif self.a.get(hexa) == "NOOP":
                        programCounter = programCounter + 1
                        print(self.flagReg)

                    # this instruction ends the entire virtual machine program
                    elif self.a.get(hexa) == "END":
                        print(self.flagReg)
                        break

                    if index < endRow and programCounter > 127:
                        index = index + 1
                        programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        index = index + 1

                self.last_executed = proc
                proc.terminated = True
                print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                self.kill_p(proc.process_ID)
                break

            else:
                self.Q2.insert(i, proc)


    def debug_p(self, process_ID):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            if str(proc.process_ID) == str(process_ID):
                self.Q1.insert(i, (proc.process_priority, proc))
                if not proc.terminated:
                    proc = (self.Q1.pop(i))[1]
                    startRow = proc.codebaseRowCol[0]
                    endRow = proc.codelimitRowCol[0]
                    index = startRow
                    programCounter = proc.codebaseRowCol[1]
                    stackindex = proc.stackEndRowCol[1]
                    hexa = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))

                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)






                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)





                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)





                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                             sum.to_bytes(2, "big",
                                                                                                          signed=True),
                                                                                             proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)


                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                    "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                      "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                    2,
                                    "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)


                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.PUSH(hex1, proc)
                        proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                        signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            self.instruc.POP(hex1, val, proc)
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


                    self.last_executed = proc
                    if index < endRow and programCounter > 127:
                        index = index + 1
                        programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        index = index + 1
                    proc.codebaseRowCol = (index, programCounter)
                    self.Q1.insert(i, (proc.process_priority, proc))
                    break

            else:
                self.Q1.insert(i, (proc.process_priority, proc))

        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if str(proc.process_ID) == str(process_ID):
                self.Q2.insert(i, proc)
                if not proc.terminated:
                    proc = self.Q2.pop(i)
                    startRow = proc.codebaseRowCol[0]
                    endRow = proc.codelimitRowCol[0]
                    index = startRow
                    programCounter = proc.codebaseRowCol[1]
                    stackindex = proc.stackEndRowCol[1]
                    hexa = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))

                    if self.a.get(hexa) == "MOV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.instruc.MOV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ADD":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUB":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)



                    elif self.a.get(hexa) == "MUL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIV":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)






                    elif self.a.get(hexa) == "AND":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "OR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        hex2 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                        programCounter = programCounter + 3
                        print(self.flagReg)





                    elif self.a.get(hexa) == "MOVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "ADDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "SUBI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)





                    elif self.a.get(hexa) == "MULI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "DIVI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)





                    elif self.a.get(hexa) == "ANDI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                              sum.to_bytes(2, "big",
                                                                                                           signed=True),
                                                                                              proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    elif self.a.get(hexa) == "ORI":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                             sum.to_bytes(2, "big",
                                                                                                          signed=True),
                                                                                             proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)




                    # Execution of Branch instructions
                    elif self.a.get(hexa) == "BZ":
                        if self.flagReg[1] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    elif self.a.get(hexa) == "BNZ":
                        if self.flagReg[1] == 0:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "BC":
                        if self.flagReg[0] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)



                    elif self.a.get(hexa) == "BS":
                        if self.flagReg[2] == 1:
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                            programCounter = sum
                        else:
                            programCounter = programCounter + 4
                        print(self.flagReg)


                    # Jump instruction executed
                    elif self.a.get(hexa) == "JMP":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)


                    elif self.a.get(hexa) == "CALL":
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)

                        proc.stack.put(programCounter)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                    "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                      "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                    2,
                                    "big")
                        stackindex = stackindex - 1
                        location = proc.codebaseRowCol[1] + sum
                        programCounter = location
                        print(self.flagReg)


                    # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                    # After that they are then stored in specific location and Memory Array.
                    elif self.a.get(hexa) == "MOVL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location // 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                    elif self.a.get(hexa) == "MOVS":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.MOVS(hex1, proc)
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3],
                            "big", signed=True)
                        location = proc.dataBaseRowCol[1] + sum
                        pgNum = location / 128
                        pgOffset = location % 128
                        frameNum = proc.pageTable[pgNum]
                        self.byte_arrayMem[frameNum][pgOffset] = val
                        programCounter = programCounter + 4
                        print(self.flagReg)


                    # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                    # register is passed to Shift left method whose value will be shifted one place to the left
                    elif self.a.get(hexa) == "SHL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # register is passed to Shift Right method whose value will be shifted one place to the right
                    elif self.a.get(hexa) == "SHR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # register is passed to Rotate left method whose value will be rotated one place to the left
                    elif self.a.get(hexa) == "RTL":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    # register is passed to Rotate right method whose value will be rotated one place to the right
                    elif self.a.get(hexa) == "RTR":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                              proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                    elif self.a.get(hexa) == "INC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.INC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)



                    elif self.a.get(hexa) == "DEC":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        self.instruc.DEC(hex1, proc)
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "PUSH":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        val = self.instruc.PUSH(hex1, proc)
                        proc.stack.put(val)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            if stackindex != -1:
                                self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                            else:
                                stackindex = 127
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                        signed=False)
                        stackindex = stackindex - 1
                        programCounter = programCounter + 2
                        print(self.flagReg)


                    elif self.a.get(hexa) == "POP":
                        hex1 = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                        if not proc.stack.empty():
                            val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                stackindex = stackindex + 1
                            else:
                                if stackindex == 127:
                                    stackindex = 0
                                else:
                                    stackindex = stackindex + 1
                            self.instruc.POP(hex1, val, proc)
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



                    self.last_executed = proc
                    if index < endRow and programCounter > 127:
                        index = index + 1
                        programCounter = 0

                    if index == endRow and programCounter > proc.codelimitRowCol[1]:
                        index = index + 1
                    proc.codebaseRowCol = (index, programCounter)
                    self.Q2.insert(i, proc)
                    break

            else:
                self.Q2.insert(i, proc)



    def debug_a(self):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            if not proc.terminated:
                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                index = startRow
                programCounter = proc.codebaseRowCol[1]
                if proc.stackindexCol == -1:
                    stackindex = proc.stackEndRowCol[1]
                else:
                    stackindex = proc.stackindexCol
                hexa = self.int_to_hex(
                    int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))

                if self.a.get(hexa) == "MOV":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.instruc.MOV(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "ADD":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "SUB":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)



                elif self.a.get(hexa) == "MUL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "DIV":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)






                elif self.a.get(hexa) == "AND":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)





                elif self.a.get(hexa) == "OR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)





                elif self.a.get(hexa) == "MOVI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "ADDI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "SUBI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)





                elif self.a.get(hexa) == "MULI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "DIVI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)





                elif self.a.get(hexa) == "ANDI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "ORI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True),
                                                                                         proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                # Execution of Branch instructions
                elif self.a.get(hexa) == "BZ":
                    if self.flagReg[1] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)


                elif self.a.get(hexa) == "BNZ":
                    if self.flagReg[1] == 0:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "BC":
                    if self.flagReg[0] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "BS":
                    if self.flagReg[2] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)


                # Jump instruction executed
                elif self.a.get(hexa) == "JMP":
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.codebaseRowCol[1] + sum
                    programCounter = location
                    print(self.flagReg)


                elif self.a.get(hexa) == "CALL":
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    proc.stack.put(programCounter)
                    if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                        self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                           "big")
                    else:
                        if stackindex != -1:
                            self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                             "big")
                        else:
                            stackindex = 127
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                2,
                                "big")
                    stackindex = stackindex - 1
                    location = proc.codebaseRowCol[1] + sum
                    programCounter = location
                    proc.stackindexCol = stackindex
                    print(self.flagReg)


                # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                # After that they are then stored in specific location and Memory Array.
                elif self.a.get(hexa) == "MOVL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.dataBaseRowCol[1] + sum
                    pgNum = location // 128
                    pgOffset = location % 128
                    frameNum = proc.pageTable[pgNum]
                    self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)


                # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                elif self.a.get(hexa) == "MOVS":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    val = self.instruc.MOVS(hex1, proc)
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.dataBaseRowCol[1] + sum
                    pgNum = location / 128
                    pgOffset = location % 128
                    frameNum = proc.pageTable[pgNum]
                    self.byte_arrayMem[frameNum][pgOffset] = val
                    programCounter = programCounter + 4
                    print(self.flagReg)


                # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                # register is passed to Shift left method whose value will be shifted one place to the left
                elif self.a.get(hexa) == "SHL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # register is passed to Shift Right method whose value will be shifted one place to the right
                elif self.a.get(hexa) == "SHR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # register is passed to Rotate left method whose value will be rotated one place to the left
                elif self.a.get(hexa) == "RTL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)


                # register is passed to Rotate right method whose value will be rotated one place to the right
                elif self.a.get(hexa) == "RTR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                elif self.a.get(hexa) == "INC":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.instruc.INC(hex1, proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                elif self.a.get(hexa) == "DEC":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.instruc.DEC(hex1, proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)


                elif self.a.get(hexa) == "PUSH":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    val = self.instruc.PUSH(hex1, proc)
                    proc.stack.put(val)
                    if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                        self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                    else:
                        if stackindex != -1:
                            self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            stackindex = 127
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                    signed=False)
                    stackindex = stackindex - 1
                    programCounter = programCounter + 2
                    proc.stackindexCol = stackindex
                    print(self.flagReg)


                elif self.a.get(hexa) == "POP":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    if not proc.stack.empty():
                        val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            stackindex = stackindex + 1
                        else:
                            if stackindex == 127:
                                stackindex = 0
                            else:
                                stackindex = stackindex + 1
                        self.instruc.POP(hex1, val, proc)
                    programCounter = programCounter + 2
                    proc.stackindexCol = stackindex
                    print(self.flagReg)


                # this instruction does nothing and program counter moves to the next instruction
                elif self.a.get(hexa) == "NOOP":
                    programCounter = programCounter + 1
                    print(self.flagReg)


                # this instruction ends the entire virtual machine program
                elif self.a.get(hexa) == "END":
                    print(self.flagReg)
                    print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")




                if index < endRow and programCounter > 127:
                    index = index + 1
                    programCounter = 0

                if index == endRow and programCounter > proc.codelimitRowCol[1]:
                    index = index + 1
                proc.codebaseRowCol = (index, programCounter)
                self.last_executed = proc
                self.Q1.insert(i, (proc.process_priority, proc))




        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if not proc.terminated:
                startRow = proc.codebaseRowCol[0]
                endRow = proc.codelimitRowCol[0]
                index = startRow
                programCounter = proc.codebaseRowCol[1]
                if proc.stackindexCol == -1:
                    stackindex = proc.stackEndRowCol[1]
                else:
                    stackindex = proc.stackindexCol
                hexa = self.int_to_hex(
                    int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))

                if self.a.get(hexa) == "MOV":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.instruc.MOV(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "ADD":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "SUB":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)



                elif self.a.get(hexa) == "MUL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)




                elif self.a.get(hexa) == "DIV":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)






                elif self.a.get(hexa) == "AND":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)





                elif self.a.get(hexa) == "OR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    hex2 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                    programCounter = programCounter + 3
                    print(self.flagReg)





                elif self.a.get(hexa) == "MOVI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "ADDI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "SUBI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)





                elif self.a.get(hexa) == "MULI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "DIVI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)





                elif self.a.get(hexa) == "ANDI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                          sum.to_bytes(2, "big",
                                                                                                       signed=True),
                                                                                          proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                elif self.a.get(hexa) == "ORI":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                         sum.to_bytes(2, "big",
                                                                                                      signed=True),
                                                                                         proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)




                # Execution of Branch instructions
                elif self.a.get(hexa) == "BZ":
                    if self.flagReg[1] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)


                elif self.a.get(hexa) == "BNZ":
                    if self.flagReg[1] == 0:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "BC":
                    if self.flagReg[0] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)



                elif self.a.get(hexa) == "BS":
                    if self.flagReg[2] == 1:
                        sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                             signed=True) + int.from_bytes(
                            self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                        programCounter = sum
                    else:
                        programCounter = programCounter + 4
                    print(self.flagReg)


                # Jump instruction executed
                elif self.a.get(hexa) == "JMP":
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.codebaseRowCol[1] + sum
                    programCounter = location
                    print(self.flagReg)


                elif self.a.get(hexa) == "CALL":
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)

                    proc.stack.put(programCounter)
                    if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                        self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                           "big")
                    else:
                        if stackindex != -1:
                            self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                             "big")
                        else:
                            stackindex = 127
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                2,
                                "big")
                    stackindex = stackindex - 1
                    location = proc.codebaseRowCol[1] + sum
                    programCounter = location
                    proc.stackindexCol = stackindex
                    print(self.flagReg)


                # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                # After that they are then stored in specific location and Memory Array.
                elif self.a.get(hexa) == "MOVL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.dataBaseRowCol[1] + sum
                    pgNum = location // 128
                    pgOffset = location % 128
                    frameNum = proc.pageTable[pgNum]
                    self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                    programCounter = programCounter + 4
                    print(self.flagReg)


                # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                elif self.a.get(hexa) == "MOVS":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    val = self.instruc.MOVS(hex1, proc)
                    sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                         signed=True) + int.from_bytes(
                        self.byte_arrayMem[index][programCounter + 3],
                        "big", signed=True)
                    location = proc.dataBaseRowCol[1] + sum
                    pgNum = location / 128
                    pgOffset = location % 128
                    frameNum = proc.pageTable[pgNum]
                    self.byte_arrayMem[frameNum][pgOffset] = val
                    programCounter = programCounter + 4
                    print(self.flagReg)


                # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                # register is passed to Shift left method whose value will be shifted one place to the left
                elif self.a.get(hexa) == "SHL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # register is passed to Shift Right method whose value will be shifted one place to the right
                elif self.a.get(hexa) == "SHR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # register is passed to Rotate left method whose value will be rotated one place to the left
                elif self.a.get(hexa) == "RTL":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)


                # register is passed to Rotate right method whose value will be rotated one place to the right
                elif self.a.get(hexa) == "RTR":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                          proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                elif self.a.get(hexa) == "INC":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.instruc.INC(hex1, proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)



                elif self.a.get(hexa) == "DEC":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    self.instruc.DEC(hex1, proc)
                    programCounter = programCounter + 2
                    print(self.flagReg)


                elif self.a.get(hexa) == "PUSH":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    val = self.instruc.PUSH(hex1, proc)
                    proc.stack.put(val)
                    if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                        self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                    else:
                        if stackindex != -1:
                            self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                        else:
                            stackindex = 127
                            self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                    signed=False)
                    stackindex = stackindex - 1
                    programCounter = programCounter + 2
                    proc.stackindexCol = stackindex
                    print(self.flagReg)


                elif self.a.get(hexa) == "POP":
                    hex1 = self.int_to_hex(
                        int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                    if not proc.stack.empty():
                        val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                        if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                            stackindex = stackindex + 1
                        else:
                            if stackindex == 127:
                                stackindex = 0
                            else:
                                stackindex = stackindex + 1
                        self.instruc.POP(hex1, val, proc)
                    programCounter = programCounter + 2
                    proc.stackindexCol = stackindex
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
                proc.codebaseRowCol = (index, programCounter)
                self.last_executed = proc
                self.Q2.insert(i, proc)


    def run_a(self):
        while len(self.Q1) != 0 or len(self.Q2) != 0:
            # Number is read from memory and converted to hex through a function that we have made.
            # This hex is put into the dictionary to get its corresponding opcode.
            if len(self.Q1) != 0:
                proc = self.Q1.pop(0)[1]
                if proc.terminated == True:
                    print("process already terminated")
                else:
                    startRow = proc.codebaseRowCol[0]
                    endRow = proc.codelimitRowCol[0]
                    programCounter = proc.codebaseRowCol[1]
                    index = startRow
                    stackindex = proc.stackEndRowCol[1]
                    while index <= endRow:
                        hexa = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))
                        print(self.a.get(hexa))

                        if self.a.get(hexa) == None:
                            print("Syntax Error")
                            break
                        if self.a.get(hexa) == "MOV":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.instruc.MOV(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)



                        elif self.a.get(hexa) == "ADD":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "SUB":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MUL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)



                        elif self.a.get(hexa) == "DIV":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)





                        elif self.a.get(hexa) == "AND":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "OR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MOVI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "ADDI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        elif self.a.get(hexa) == "SUBI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MULI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "DIVI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "ANDI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        elif self.a.get(hexa) == "ORI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                                 sum.to_bytes(2, "big",
                                                                                                              signed=True),
                                                                                                 proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        # Execution of Branch instructions
                        elif self.a.get(hexa) == "BZ":
                            if self.flagReg[1] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)

                        elif self.a.get(hexa) == "BNZ":
                            if self.flagReg[1] == 0:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "BC":
                            if self.flagReg[0] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "BS":
                            if self.flagReg[2] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3], "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)

                        # Jump instruction executed
                        elif self.a.get(hexa) == "JMP":
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            location = proc.codebaseRowCol[1] + sum
                            programCounter = location
                            print(self.flagReg)

                        elif self.a.get(hexa) == "CALL":
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            proc.stack.put(programCounter)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                   "big")
                            else:
                                if stackindex != -1:
                                    self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                     "big")
                                else:
                                    stackindex = 127
                                    self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                        2,
                                        "big")
                            stackindex = stackindex - 1
                            location = proc.codebaseRowCol[1] + sum
                            programCounter = location
                            print(self.flagReg)

                        # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                        # After that they are then stored in specific location and Memory Array.
                        elif self.a.get(hexa) == "MOVL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            location = proc.dataBaseRowCol[1] + sum
                            pgNum = location // 128
                            pgOffset = location % 128
                            frameNum = proc.pageTable[pgNum]
                            self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)

                        # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                        elif self.a.get(hexa) == "MOVS":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            val = self.instruc.MOVS(hex1, proc)
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            location = proc.dataBaseRowCol[1] + sum
                            pgNum = location / 128
                            pgOffset = location % 128
                            frameNum = proc.pageTable[pgNum]
                            self.byte_arrayMem[frameNum][pgOffset] = val
                            programCounter = programCounter + 4
                            print(self.flagReg)

                        # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                        # register is passed to Shift left method whose value will be shifted one place to the left
                        elif self.a.get(hexa) == "SHL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # register is passed to Shift Right method whose value will be shifted one place to the right
                        elif self.a.get(hexa) == "SHR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # register is passed to Rotate left method whose value will be rotated one place to the left
                        elif self.a.get(hexa) == "RTL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        # register is passed to Rotate right method whose value will be rotated one place to the right
                        elif self.a.get(hexa) == "RTR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                        elif self.a.get(hexa) == "INC":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.instruc.INC(hex1, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        elif self.a.get(hexa) == "DEC":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.instruc.DEC(hex1, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        elif self.a.get(hexa) == "PUSH":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            val = self.instruc.PUSH(hex1, proc)
                            proc.stack.put(val)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big")
                            else:
                                if stackindex != -1:
                                    self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big")
                                else:
                                    stackindex = 127
                                    self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                            signed=False)
                            stackindex = stackindex - 1
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        elif self.a.get(hexa) == "POP":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            if not proc.stack.empty():
                                val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                                if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                    stackindex = stackindex + 1
                                else:
                                    if stackindex == 127:
                                        stackindex = 0
                                    else:
                                        stackindex = stackindex + 1
                                self.instruc.POP(hex1, val, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        # this instruction does nothing and program counter moves to the next instruction
                        elif self.a.get(hexa) == "NOOP":
                            programCounter = programCounter + 1
                            print(self.flagReg)

                        # this instruction ends the entire virtual machine program
                        elif self.a.get(hexa) == "END":
                            print(self.flagReg)
                            proc.terminated = True

                            break

                        if index < endRow and programCounter > 127:
                            index = index + 1
                            programCounter = 0

                        if index == endRow and programCounter > proc.codelimitRowCol[1]:
                            index = index + 1


                    self.last_executed = proc
                    self.kill_p(proc.process_ID)

                    print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                    proc.terminated = True


            if len(self.Q1) == 0 and len(self.Q2) != 0:
                proc = self.Q2.pop(0)
                if proc.terminated == True:
                    print("process already terminated")
                else:
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
                        hexa = self.int_to_hex(
                            int.from_bytes(self.byte_arrayMem[index][programCounter], "big", signed=False))
                        print(self.a.get(hexa))
                        if self.a.get(hexa) == None:
                            print("Syntax Error")
                            print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                            break
                        if self.a.get(hexa) == "MOV":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.instruc.MOV(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)



                        elif self.a.get(hexa) == "ADD":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADD(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "SUB":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUB(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MUL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MUL(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)



                        elif self.a.get(hexa) == "DIV":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIV(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)





                        elif self.a.get(hexa) == "AND":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.AND(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "OR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            hex2 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.OR(hex1, hex2, proc)
                            programCounter = programCounter + 3
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MOVI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.instruc.MOVI(hex1, sum.to_bytes(2, "big", signed=True), proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "ADDI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ADDI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        elif self.a.get(hexa) == "SUBI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.SUBI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "MULI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.MULI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "DIVI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.DIVI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)




                        elif self.a.get(hexa) == "ANDI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ANDI(hex1,
                                                                                                  sum.to_bytes(2, "big",
                                                                                                               signed=True),
                                                                                                  proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        elif self.a.get(hexa) == "ORI":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            self.flagReg[3], self.flagReg[2], self.flagReg[1] = self.instruc.ORI(hex1,
                                                                                                 sum.to_bytes(2, "big",
                                                                                                              signed=True),
                                                                                                 proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)



                        # Execution of Branch instructions
                        elif self.a.get(hexa) == "BZ":
                            if self.flagReg[1] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3],
                                    "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)

                        elif self.a.get(hexa) == "BNZ":
                            if self.flagReg[1] == 0:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3],
                                    "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "BC":
                            if self.flagReg[0] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3],
                                    "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)


                        elif self.a.get(hexa) == "BS":
                            if self.flagReg[2] == 1:
                                sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                     signed=True) + int.from_bytes(
                                    self.byte_arrayMem[index][programCounter + 3],
                                    "big", signed=True)
                                programCounter = sum
                            else:
                                programCounter = programCounter + 4
                            print(self.flagReg)

                        # Jump instruction executed
                        elif self.a.get(hexa) == "JMP":
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            location = proc.codebaseRowCol[1] + sum
                            programCounter = location
                            print(self.flagReg)

                        elif self.a.get(hexa) == "CALL":
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)

                            proc.stack.put(programCounter)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                   "big")
                            else:
                                if stackindex != -1:
                                    self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = programCounter.to_bytes(2,
                                                                                                                     "big")
                                else:
                                    stackindex = 127
                                    self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = programCounter.to_bytes(
                                        2,
                                        "big")
                            stackindex = stackindex - 1
                            location = proc.codebaseRowCol[1] + sum
                            programCounter = location
                            print(self.flagReg)

                        # Now the register and element in memory array are passed in their desired instruction methods in the instruction class through its object.
                        # After that they are then stored in specific location and Memory Array.
                        elif self.a.get(hexa) == "MOVL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=False))
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=False) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=False)
                            location = proc.dataBaseRowCol[1] + sum
                            pgNum = location // 128
                            pgOffset = location % 128
                            frameNum = proc.pageTable[pgNum]
                            self.instruc.MOVL(hex1, self.byte_arrayMem[frameNum][pgOffset], proc)
                            programCounter = programCounter + 4
                            print(self.flagReg)

                        # the register is passed in the MOVS instruction to get register value and thenstore it in memeory array and specified location   elif a.get(hexa) == "MOVS"
                        elif self.a.get(hexa) == "MOVS":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            val = self.instruc.MOVS(hex1, proc)
                            sum = int.from_bytes(self.byte_arrayMem[index][programCounter + 2], "big",
                                                 signed=True) + int.from_bytes(
                                self.byte_arrayMem[index][programCounter + 3],
                                "big", signed=True)
                            location = proc.dataBaseRowCol[1] + sum
                            pgNum = location / 128
                            pgOffset = location % 128
                            frameNum = proc.pageTable[pgNum]
                            self.byte_arrayMem[frameNum][pgOffset] = val
                            programCounter = programCounter + 4
                            print(self.flagReg)

                        # Register is passed to Shift methods whose value will be shifted one place to the left or vice versa.
                        # register is passed to Shift left method whose value will be shifted one place to the left
                        elif self.a.get(hexa) == "SHL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHL(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # register is passed to Shift Right method whose value will be shifted one place to the right
                        elif self.a.get(hexa) == "SHR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.SHR(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # register is passed to Rotate left method whose value will be rotated one place to the left
                        elif self.a.get(hexa) == "RTL":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTL(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        # register is passed to Rotate right method whose value will be rotated one place to the right
                        elif self.a.get(hexa) == "RTR":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.flagReg[3], self.flagReg[2], self.flagReg[1], self.flagReg[0] = self.instruc.RTR(hex1,
                                                                                                                  proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        # Register is passed to Increment/Decrement methods whose value will be Incremented/Decremented by 1.
                        elif self.a.get(hexa) == "INC":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.instruc.INC(hex1, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)


                        elif self.a.get(hexa) == "DEC":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            self.instruc.DEC(hex1, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        elif self.a.get(hexa) == "PUSH":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            val = self.instruc.PUSH(hex1, proc)
                            if proc.stack.empty() == False:
                                proc.stack.put(val)
                            if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                        signed=False)
                            else:
                                if stackindex != -1:
                                    self.byte_arrayMem[proc.stackEndRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                          signed=False)
                                else:
                                    stackindex = 127
                                    self.byte_arrayMem[proc.stackStartRowCol[0]][stackindex] = val.to_bytes(2, "big",
                                                                                                            signed=False)
                            stackindex = stackindex - 1
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        elif self.a.get(hexa) == "POP":
                            hex1 = self.int_to_hex(
                                int.from_bytes(self.byte_arrayMem[index][programCounter + 1], "big", signed=True))
                            if not proc.stack.empty():
                                val = int(proc.stack.get()).to_bytes(2, "big", signed=True)
                                if proc.stackStartRowCol[0] == proc.stackEndRowCol[0]:
                                    stackindex = stackindex + 1
                                else:
                                    if stackindex == 127:
                                        stackindex = 0
                                    else:
                                        stackindex = stackindex + 1
                                self.instruc.POP(hex1, val, proc)
                            programCounter = programCounter + 2
                            print(self.flagReg)

                        # this instruction does nothing and program counter moves to the next instruction
                        elif self.a.get(hexa) == "NOOP":
                            programCounter = programCounter + 1
                            print(self.flagReg)

                        # this instruction ends the entire virtual machine program
                        elif self.a.get(hexa) == "END":
                            print(self.flagReg)
                            proc.terminated = True
                            self.kill_p(proc.process_ID)
                            break

                        if index < endRow and programCounter > 127:
                            index = index + 1
                            programCounter = 0

                        if index == endRow and programCounter > proc.codelimitRowCol[1]:
                            print("process " + str(proc.process_ID) + " " + str(proc.process_filename) + " Executed")
                            proc.terminated =True
                            self.kill_p(proc.process_ID)
                            index = index + 1

                        if timetaken == timeSlice and index <= endRow:
                            proc.codebaseRowCol = (index, programCounter)
                            proc.stackindexCol = stackindex
                            self.Q2.append(proc)
                            break
                        else:
                            timetaken = timetaken + 2

                    self.last_executed = proc


    def kill_p(self, process_ID):
        if len(self.Q1) != 0:
            for i in range(len(self.Q1)):
                proc = (self.Q1.pop(i))[1]
                if str(proc.process_ID) == str(process_ID):
                    proc.terminated = True
                    for j in range(len(proc.pageTable)):
                        frameNum = proc.pageTable[j]
                        self.frameTable[frameNum] = False
                        for col in range(128):
                            self.byte_arrayMem[frameNum][col] = (0).to_bytes(2,"big", signed=False)
                    print("process killed successfully!")
                    break
                else:
                    self.Q1.insert(i, (proc.process_priority, proc))
        if len(self.Q2) != 0:
            for i in range(len(self.Q2)):
                proc = self.Q2.pop(i)
                if str(proc.process_ID) == str(process_ID):
                    proc.terminated = True
                    for j in range(len(proc.pageTable)):
                        frameNum = proc.pageTable[j]
                        self.frameTable[frameNum] = False
                        for col in range(128):
                            self.byte_arrayMem[frameNum][col] = (0).to_bytes(2,"big", signed=False)
                    print("process killed successfully!")
                    break
                else:
                    self.Q2.insert(i, proc)

    def list_a(self):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            print(proc.process_filename)
            print(proc.registers.registerArr)
            self.Q1.insert(i, (proc.process_priority, proc))
        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            print(proc.process_filename)
            print(proc.registers.registerArr)
            self.Q2.insert(i, proc)

    def list_b(self):
        for i in range(len(self.blocked)):
            proc = self.blocked.pop(i)
            print(proc.process_filename)
            print(proc.registers.registerArr)
            self.blocked.insert(i, proc)

    def list_r(self):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            print(proc.process_filename)
            print(proc.registers.registerArr)
            self.Q1.insert(i, (proc.process_priority, proc))
        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            print(proc.process_filename)
            print(proc.registers.registerArr)
            self.Q2.insert(i, proc)

    def list_e(self):
        print(self.last_executed.process_filename)
        print(self.last_executed.registers.registerArr)

    def display_p(self, process_ID):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            if str(proc.process_ID) == str(process_ID):
                proc.print()
                self.Q1.insert(i, (proc.process_priority, proc))
                break
            else:
                self.Q1.insert(i, (proc.process_priority, proc))

        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if str(proc.process_ID) == str(process_ID):
                proc.print()
                self.Q2.insert(i, proc)
                break
            else:
                self.Q2.insert(i, proc)

    def display_m(self, process_ID):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            if str(proc.process_ID) == str(process_ID):
                for j in range(len(proc.pageTable)):
                    print("page number: " + str(j) + "   frame number " + str(proc.pageTable[j]))
                self.Q1.insert(i, (proc.process_priority, proc))
                break
            else:
                self.Q1.insert(i, (proc.process_priority, proc))

        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if str(proc.process_ID) == str(process_ID):
                for j in range(len(proc.pageTable)):
                    print("page number: " + str(j) + "   frame number " + str(proc.pageTable[j]))
                self.Q2.insert(i, proc)
                break
            else:
                self.Q2.insert(i, proc)

    def dump(self, process_ID):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            if str(proc.process_ID) == str(process_ID):
                f = open(str(proc.process_filename) + "_" + "dump", "a")
                f.write("\nprocess ID = " + str(proc.process_ID) + "\n")
                f.write("process name = " + str(proc.process_filename) + "\n")
                f.write("process priority = " + str(proc.process_priority) + "\n")
                f.write("process size = " + str(proc.process_Size) + "\n")
                f.write("registers:-\n")
                f.writelines(str(proc.registers.registerArr))
                f.write("\ncode size = " + str(proc.codeSize) + "\n")
                f.write("data size = " + str(proc.dataSize) + "\n")
                f.write("Memory:\n")
                for j in range(len(proc.pageTable)):
                    frameNum = proc.pageTable[j]
                    f.writelines(str(self.byte_arrayMem[frameNum]) + "\n")
                f.close()
                print("Dumped Successfully!")
                self.Q1.insert(i, (proc.process_priority, proc))
                break
            else:
                self.Q1.insert(i, (proc.process_priority, proc))

        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            if str(proc.process_ID) == str(process_ID):
                f = open(str(proc.process_filename) + "_" + "dump", "a")
                f.write("\nprocess ID = " + str(proc.process_ID) + "\n")
                f.write("process name = " + str(proc.process_filename) + "\n")
                f.write("process priority = " + str(proc.process_priority) + "\n")
                f.write("process size = " + str(proc.process_Size) + "\n")
                f.write("registers:-\n")
                f.writelines(str(proc.registers.registerArr))
                f.write("\ncode size = " + str(proc.codeSize) + "\n")
                f.write("data size = " + str(proc.dataSize) + "\n")
                f.write("Memory:\n")
                for j in range(len(proc.pageTable)):
                    frameNum = proc.pageTable[j]
                    f.writelines(str(self.byte_arrayMem[frameNum]) + "\n")
                f.close()
                print("Dumped Successfully!")
                self.Q2.insert(i, proc)
                break
            else:
                self.Q2.insert(i, proc)


    def frames_f(self):
        print("True = Frame Occupied     False = Empty Frame")
        print(self.frameTable)

    def mem(self):
        if self.last_executed == None:
            print("first execute a process and then try again")
        else:
            print("Process Size = " + str(self.last_executed.process_Size))

    def frames_a(self):
        for i in range(len(self.Q1)):
            proc = (self.Q1.pop(i))[1]
            print("Process ID: " + str(proc.process_ID))
            for j in range(len(proc.pageTable)):
                print("frame number: " + str(proc.pageTable[j]))
            self.Q1.insert(i, (proc.process_priority, proc))

        for i in range(len(self.Q2)):
            proc = self.Q2.pop(i)
            print("Process ID: " + str(proc.process_ID))
            for j in range(len(proc.pageTable)):
                print("frame number: " + str(proc.pageTable[j]))
            self.Q2.insert(i, proc)

    def registers(self):
        if self.last_executed == None:
            print("no process executed yet....all registers are empty")
        else:
            print("Flag Register:")
            print(self.flagReg)
            print("Registers:")
            print(self.last_executed.registers.registerArr)

    def block(self, process_ID):
        if len(self.Q1) != 0:
            for i in range(len(self.Q1)):
                proc = (self.Q1.pop(i))[1]
                if str(proc.process_ID) == str(process_ID):
                    self.blocked.append(proc)
                    print("process blocked successfully!")
                    break
                else:
                    self.Q1.insert(i, (proc.process_priority, proc))
        elif len(self.Q2) != 0:
            for i in range(len(self.Q2)):
                proc = self.Q2.pop(i)
                if str(proc.process_ID) == str(process_ID):
                    self.blocked.append(proc)
                    print("process blocked successfully!")
                    break
                else:
                    self.Q2.insert(i, proc)

    def unblock(self, process_ID):
        if len(self.blocked) != 0:
            for i in range(len(self.blocked)):
                proc = self.blocked.pop(i)
                if str(proc.process_ID) == str(process_ID):
                    if proc.process_priority >= 0 and proc.process_priority <= 15:
                        self.Q1.append((proc.process_priority, proc))
                        print("process unblocked successfully!")
                    if proc.process_priority > 15 and proc.process_priority <= 31:
                        self.Q2.append(proc)
                        print("process unblocked successfully!")
                    break
                else:
                    self.blocked.insert(proc)

    def shutdown(self):
        if len(self.Q1) != 0:
            while len(self.Q1) != 0:
                proc = (self.Q1.pop(0))[1]
                proc.terminated = True
                for j in range(len(proc.pageTable)):
                    frameNum = proc.pageTable[j]
                    self.frameTable[frameNum] = False
                    for col in range(128):
                        self.byte_arrayMem[frameNum][col] = (0).to_bytes(2, "big", signed=False)
                print("process ID = " + str(proc.process_ID))

        if len(self.Q2) != 0:
            while len(self.Q2) != 0:
                proc = self.Q2.pop(0)
                proc.terminated = True
                for j in range(len(proc.pageTable)):
                    frameNum = proc.pageTable[j]
                    self.frameTable[frameNum] = False
                    for col in range(128):
                        self.byte_arrayMem[frameNum][col] = (0).to_bytes(2, "big", signed=False)
                print("process ID = " + str(proc.process_ID))

        print("Shutdown Sucessful!")
        quit()



    #dictionary with command keyword and its corresponding function to be called
    dicti = {"load": load, "run -p": run_p, "debug -p": debug_p, "debug -a": debug_a,
             "run -a": run_a, "kill -p": kill_p, "list -a": list_a, "list -b": list_b,
             "list -r": list_r, "list -e": list_e, "display -p": display_p, "display -m": display_m,
             "dump": dump, "frames -f": frames_f, "mem": mem, "frames -a": frames_a,
             "registers": registers, "block": block, "unblock": unblock, "shutdown": shutdown}

    #dictionary with command keyword with its corresponding boolean value which indicates whether the command has
    #an argument aswell. True means yes and False means No
    dicti1 = {"load": True, "run -p": True, "debug -p": True, "debug -a": False,
             "run -a": False, "kill -p": True, "list -a": False, "list -b": False,
             "list -r": False, "list -e": False, "display -p": True, "display -m": True,
             "dump": True, "frames -f": False, "mem": False, "frames -a": False,
             "registers": False,  "block": True, "unblock": True, "shutdown": False}


    #Main prgram from where the OS starts.....user inputs commands and its corresponding action is done by calling the command
    #functions given above
    def run(self):

        while True:
            inp = input(">")
            command= ""
            arg = ""
            for i in range(len(inp)):
                if inp[i] == " ":
                    if inp[i+1] == "-":
                        command = inp[0:i+3]
                        if command in self.dicti:
                            if self.dicti1[command]:
                                arg = inp[i + 4:]
                    elif inp[i+1] == " ":
                        command = inp[0:i]
                    elif inp[i+1] != " " and inp[i+1] != "-":
                        command = inp[0:i]
                        if command in self.dicti:
                            if self.dicti1[command]:
                                arg = inp[i + 1:]


                elif i == len(inp)-1:
                    command = inp

                if len(command) != 0:
                    break

            if command in self.dicti:
                if len(arg) != 0:
                    func = self.dicti[command]
                    func(self, arg)
                else:
                    func = self.dicti[command]
                    func(self)

            else:
                print("invalid command....please try again")





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