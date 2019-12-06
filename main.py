# -*- coding: utf-8 -*-

RS = {}

rs = {}
rs = {'exec':0, 'BUSY': 'N', 'op': 'NULL', 'Vj':0, 'Vk':0, 'Qj':-1, 'Qk':-1, 'DEST':-1, 'A':0}

myNANDList = [rs.copy() for i in range(2)]
myADDList = [rs.copy() for i in range(3)]
myBEQList = [rs.copy() for i in range(2)]
myLWList = [rs.copy() for i in range(2)]
mySWList = [rs.copy() for i in range(2)]
myJMPList = [rs.copy() for i in range(2)]
myMULTList = [rs.copy() for i in range(2)]

RS['NAND'] = myNANDList
RS['BEQ'] = myBEQList
RS['MULT'] = myMULTList
RS['JMP'] = myJMPList
RS['SW'] = mySWList
RS['LW'] = myLWList
RS['ADD'] = myADDList


dataMemory = [0] * 65536

RF = {}

#R2 is a register that is used by ROB1 and has the value of 25
RF['R0'] = [-1,0]
RF['R1'] = [-1,1]
RF['R2'] = [-1,2]
RF['R3'] = [-1,3]
RF['R4'] = [-1,4]
RF['R5'] = [-1,5]
RF['R6'] = [-1,6]
RF['R7'] = [-1,7]

ROB = {}
ROB[0] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[1] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[2] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[3] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[4] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[5] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[6] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
ROB[7] = {'Type': 'LD', 'DEST':0, 'Value': 25, 'Ready': 'N'}
usedROB = 0

head = []
head.append(0)
tail = []
tail.append(0)

instructions = []

pc = 0
cycle = 0



def fillRS(rs, instruction, instructionType):        
        
    if((instructionType == 'ADD') or (instructionType == 'NAND') or (instructionType == 'MULT')):
        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        ROB[tail[0]]['Type'] = instructionType
        ROB[tail[0]]['DEST'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['DEST'] = RF[instruction[1]][0]
        if(RF[instruction[2]][0] == 0):
            rs['Vj'] = RF[instruction[2]][1]
            rs['Qj'] = -1
        
        else:
            rs['Vj'] = 0
            rs['Qj'] = RF[instruction[2]][0]
        
        
        if(RF[instruction[3]][0] == 0):
            rs['Vk'] = RF[instruction[3]][1]
            rs['Qk'] = -1
        
        else:
            rs['Vk'] = 0
            rs['Qk'] = RF[instruction[3]][0]
            
        RF[instruction[1]][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8
        
        
    elif((instructionType == 'LW') or (instructionType == 'SW') or (instructionType == 'BEQ') ):
        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        rs['A'] = instruction[3]    # the immediate value
        ROB[tail[0]]['Type'] = instructionType
        ROB[tail[0]]['DEST'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
        
        
        rs['DEST'] = RF[instruction[1]][0]
        if(RF[instruction[2]][0] == 0):
            rs['Vj'] = RF[instruction[2]][1]
            rs['Qj'] = -1
        
        else:
            rs['Vj'] = 0
            rs['Qj'] = RF[instruction[2]][0]
            
        RF[instruction[1]][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8
    
    elif(instructionType == 'JMP'):
        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        rs['A'] = instruction[1]    # the immediate value
        ROB[tail[0]]['Type'] = instructionType
        ROB[tail[0]]['DEST'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
            
        RF[instruction[1]][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8
    

    #TODO: JALR and RET
    


def decodeInstructionType(instruction):
    # if it is arithmetic
    if((instruction[0] =='ADD' ) or (instruction[0] == 'SUB') or (instruction[0] == 'ADDI')):
        return 'ADD'
    
    # if it is a branch
    if((instruction[0] =='JMP') or (instruction[0] == 'JALR') or (instruction[0] =='RET')):
        return 'JMP'
    
    # if it is anything else
    else:
        return instruction[0]

# a function that takes a file name and reads the instruction in it and puts them in a list
def readInstructionsFromFile(instructions, fileName):
    f = open(fileName, "r+")
    for line in f:
        parts = line.split()
        if(len(parts) == 4):
            thisInstruction = []
            thisInstruction.append(parts[0])
            thisInstruction.append(parts[1][:-1])
            thisInstruction.append(parts[2][:-1])
            thisInstruction.append(parts[3])
            instructions.append(thisInstruction)
        elif(len(parts) == 2):
            thisInstruction = []
            thisInstruction.append(parts[0])
            thisInstruction.append(parts[1])
            instructions.append(thisInstruction)
        else:
            thisInstruction = []
            thisInstruction.append(parts[0])
            instructions.append(thisInstruction)
            
    
    
 
    
readInstructionsFromFile(instructions, 'instructions.txt')    
while pc<4:
    
    # firstly, handle issuing
    instruction1 = instructions[pc]
    instruction1Type = decodeInstructionType(instruction1)
    #to do: if inst1 is a JMP, then fetch inst2 from prediction instead of pc+1
    instruction2 = instructions[pc + 1]
    instruction2Type = decodeInstructionType(instruction1)
    
    instruction1Issued = 0
    instruction2Issued = 0
    
    if(usedROB < 8): #we have enough space in ROB
        
        
        for rs in RS[instruction1Type]:
            if(rs['BUSY'] == 'N'):
                instruction1Issued = 1
                usedROB += 1
                fillRS(rs, instruction1, instruction1Type)
                break
        
        if(usedROB < 8) and instruction1Issued:
            
            for rs in RS[instruction2Type]:
                if(rs['BUSY'] == 'N'):
                    fillRS(rs, instruction2, instruction2Type)
                    instruction2Issued = 1;
                    usedROB += 1
                    break;
    
    
    if(instruction2Issued):
        pc += 2
    elif(instruction1Issued):
        pc += 1
        
    # secondly, handle commiting:
    
        
    cycle += 1
    print(cycle)
    
    

        
        
        