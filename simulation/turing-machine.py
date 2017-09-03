class Tape:
    def __init__(self, content):
        self.content = {}
        for i in range(len(content)):
            self.content[i] = content[i]
    def __getitem__(self, key):
        return self.content[key] if key in self.content else 'B'
    def __setitem__(self, key, value):
        if value =='B':
            if key in self.content:
                del self.content[key]
        else:
            self.content[key] = value
    def __str__(self):
        left = min(self.content.keys()) - 1
        right = max(self.content.keys()) + 1
        stringRep = ''
        for i in range(left, right - left):
            stringRep += self[i]
        return stringRep

class TuringMachine:
    def __init__(self, filename):
        self.instructions = {}
        with open(filename) as f:
            lines = [x.strip().split(',') for x in f.readlines()]
            self.state = lines[0][0]
            self.acceptingStates = lines[1]
            for line in lines[2:]:
                key = (line[0], line[1])
                if len(line) == 3:
                    self.instructions[key] = 'halt'
                else:
                    self.instructions[key] = (line[2],line[3], 1 if line[4] == 'R' else -1)

    def start(self, tape, verbose = False):
        self.position = 0
        self.tape = tape
        self.halted = False
        self.stepCount = 0
        self.verbose = verbose

    def executeStep(self):
        if self.verbose:
            print self.tape
        if self.halted:
            return self.state in self.acceptingStates
        self.stepCount += 1
        key = (self.state, self.tape[self.position])
        instruction = self.instructions[key]
        if instruction == 'halt':
            self.halted = True
            return self.state in self.acceptingStates
        self.state = instruction[0]
        self.tape[self.position] = instruction[1]
        self.position += instruction[2]

    def execute(self):
        while not self.halted:
            last = self.executeStep()
        return last

if __name__=='__main__':
    t = Tape('aaaaaaaaaabbbbbbbbbb')
    M = TuringMachine('example 5.txt')
    M.start(t, True)
    print(M.execute())
