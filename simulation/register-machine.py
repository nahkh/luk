import re


class RegisterMachine:
    
    def __init__(self, filename):
        self.instructions = {}
        self.registers = {}
        self.halted = False

        pattern = re.compile('^(\d+) \(([\d, ]+)\)(.*)$')
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                match = pattern.match(line.strip())
                if match == None:
                    continue
                instructionKey = match.group(1)
                instruction = match.group(2).split(', ')
                comment = match.group(3).strip()
                if instructionKey in self.instructions:
                    raise Exception('Duplicate instruction ' + instructionKey)
                self.instructions[instructionKey] = {
                    'step': instruction,
                    'comment': comment,
                    'original': '(%s)' % match.group(2)
                }


    def start(self, *args):
        i = 0
        for arg in args:
            i += 1
            self.registers['%d' % i] = arg
        self.currentInstruction = '1';
        self.stepCount = 0

    def executeStep(self):
        self.stepCount += 1
        instruction = self.getInstruction();
        if instruction == None:
            self.halted = True
            return self.getStateArray()
            
        #print '(%d) Executing %s %s %s' % (self.stepCount, self.currentInstruction, instruction['original'], instruction['comment'])
        #self.printState()
        step = instruction['step']
        register = step[0]
        if len(step) == 2:
            self.registers[register] += 1
            self.currentInstruction = step[1]

        if len(step) == 3:
            if self.registers[register] > 0:
                self.registers[register] -= 1
                self.currentInstruction = step[1]
            else:
                self.currentInstruction = step[2]

    def getInstruction(self):
        if self.currentInstruction in self.instructions:
            return self.instructions[self.currentInstruction]


    def execute(self, limit = None):
        if limit != None:
            executeTo = self.stepCount + limit
        while (not self.halted) and (limit == None or executeTo > self.stepCount):
            lastState = self.executeStep()
        return lastState

    def getStateArray(self):
        registers = []
        for i in range(1, len(self.registers) + 1):
            registers.append(self.registers['%d' % i])
        return registers

    def printState(self):
        print self.getStateArray()
    

def initialRegisters(encoding, word, alphabetSize, registerCount):
    if len(word) == 0:
        return [0] * registerCount
    accumulator = 0
    for i in range(len(word) - 1, 0, -1):
        accumulator = accumulator * alphabetSize
        accumulator += encoding[word[i]]
    initialState = [0, encoding[word[0]], accumulator]
    while len(initialState) < registerCount:
        initialState.append(0)
    return initialState

def tapeState(decoding, registers, alphabetSize):
    left = registers[0]
    right = registers[2]
    headPosition = 0
    tape = ''
    while left > 0:
        tape = decoding[left % alphabetSize] + tape
        left = left // alphabetSize
        headPosition += 1
    tape = tape + decoding[registers[1]]
    while right > 0:
        tape = tape + decoding[right % alphabetSize]
        right = right // alphabetSize
    return tape

def acceptResult(decoding, registers, acceptingStates):
    state = decoding[registers[3]]
    return state in acceptingStates

if __name__=='__main__':
    M = RegisterMachine('example 14.txt')
    M.start(*initialRegisters({'a': 1, 'b': 2}, 'aaaabbbb', 3, 5))
    finalState = M.execute()

    print tapeState({0: ' ', 1:'a', 2:'b'}, finalState, 3)
    print acceptResult({0: 'q_0', 4: 'q_e'}, finalState, ['q_0'])
    
