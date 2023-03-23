from Register import register
from queue import LifoQueue

class pcb():

    # This PCB class is basically a block class which includes all the relevant details related to a Process(Name,Priority etc)
    def __init__(self, process_id, priority, process_file_name, processSize, codesize, datasize):
        self.process_ID = process_id
        if priority >= 0 and priority < 32:
            self.process_priority = priority
        self.process_filename = process_file_name
        self.process_Size = processSize
        self.registers = register()
        self.pageTable = []
        self.stack = LifoQueue(maxsize=50)
        self.stackStartRowCol = ()
        self.stackEndRowCol = ()
        self.codebaseRowCol = ()
        self.codelimitRowCol = ()
        self.dataBaseRowCol = ()
        self.dataLimitRowCol = ()
        self.codeSize = codesize
        self.dataSize = datasize
        self.stackindexCol = -1
        self.terminated = False

    def __lt__(self, other):
        selfPriority = self.process_priority
        otherPriority = other.process_priority
        return selfPriority < otherPriority

    def print(self):
        print("process ID = " + str(self.process_ID))
        print("process priority = " + str(self.process_priority))
        print("process name = " + str(self.process_filename))
        print("process size = " + str(self.process_Size))
        print("registers:-")
        print(self.registers.registerArr)
        print("code size " + str(self.codeSize))
        print("data size " + str(self.dataSize))

