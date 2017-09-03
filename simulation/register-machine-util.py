from __future__ import print_function
import re


class Instruction:
    def __init__(self, line):
        line = line.strip()
        match = re.match('^(\d+) \(([\d, ]+)\)(.*)$', line)
        if match == None:
            match = re.match('^(\d+) halt$', line)
            if match == None:
                raise Exception('Could not parse line ' + line)
            self.lineId = int(match.group(1))
            self.instructions = []
        else:
            self.lineId = int(match.group(1))
            self.instructions = [int(x) for x in match.group(2).split(', ')]
            self.comment = match.group(3).strip()

    def toString(self):
        if len(self.instructions) == 0:
            return '%d halt' % self.lineId
        if len(self.instructions) == 2:
            return '%d (%d, %d) %s' % (self.lineId, self.instructions[0], self.instructions[1], self.comment)
        if len(self.instructions) == 3:
            return '%d (%d, %d, %d) %s' % (self.lineId, self.instructions[0], self.instructions[1], self.instructions[2], self.comment)

    def texFormat(self):
        if len(self.instructions) == 0:
            return '$\hat{%d}$ & halt & \\\\' % self.lineId

        comment = re.sub('(q\_.)', '$\g<1>$', self.comment)
        comment = re.sub(' ([abB]) ', ' $\g<1>$ ', comment)
        
        if len(self.instructions) == 2:
            return '$\hat{%d}$ & (%d, %d) & %s \\\\' % (self.lineId, self.instructions[0], self.instructions[1], comment)
        if len(self.instructions) == 3:
            return '$\hat{%d}$ & (%d, %d, %d) & %s \\\\' % (self.lineId, self.instructions[0], self.instructions[1], self.instructions[2], comment)

    def applyReplacements(self, replacements):
        self.lineId = replacements[self.lineId]
        self.instructions = [replacements[x] for x in self.instructions]

def minify(filename, target):
    with open(filename) as f:
        rawlines = f.readlines()
    lines = [Instruction(line) for line in rawlines]
    linesDict = {}
    replacements = {}
    
    for line in lines:
       linesDict[line.lineId] = line

    index = 1
    nextIndexToUse = 1

    while len(linesDict) > 0:
        while index not in linesDict:
            index += 1
        replacements[index] = nextIndexToUse
        nextIndexToUse += 1
        del linesDict[index]

    with open(target, 'w') as f:
        for line in lines:
            line.applyReplacements(replacements)
            print(line.toString(), file=f)
        
        


def texify(filename, target):
    with open(filename) as f:
        lines = f.readlines()

    with open(target, 'w') as f:
        for line in lines:
            print(Instruction(line).texFormat(), file=f)


if __name__=='__main__':
    minify('example 14.txt','minified.txt')
    texify('minified.txt','texified.txt')
