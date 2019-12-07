# -*- coding: utf-8 -*-

RS = {}

rs = {}
rs = {'cycle': -1, 'exec': -1, 'BUSY': 'N', 'op': 'NULL', 'Vj':0, 'Vk':0, 'Qj':-1, 'Qk':-1, 'Dest':-1, 'A':0}

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
ROB[0] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[1] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[2] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[3] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[4] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[5] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[6] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
ROB[7] = {'Type': 'NULL', 'Dest': 'R5', 'Value': 0, 'Ready': 'N', 'PC': -1}
usedROB = 0

head = []
head.append(0)
tail = []
tail.append(0)

instructions = []

pc = 0
cycle = 0


def readDataFromFile(fileName):
    f = open(fileName, "r+")
    for line in f:
        parts = line.split()
        dataMemory[int(parts[0])] = int(parts[1])

def clearRF_RS_ROB():
    for key,value in RF.items():
        RF[key][0] = -1
    
    for key, value in RS.items():
        for rs in value:
            rs['exec'] = -1
            rs['BUSY'] =  'N'
            rs['op'] =  'NULL'
            rs['Vj'] = 0
            rs['Vk'] = 0
            rs['Qj'] = -1
            rs['Qk'] = -1
            rs['Dest'] = -1
            rs['A'] = 0
            
    for key, value in ROB.items():
        ROB[key] = {'Type': 'LD', 'Dest':0, 'Value': 25, 'Ready': 'N', 'PC': -1}
        
def getDelay(myType):
    if((myType == 'LW') or (myType == 'SW')):
        return 3
    elif((myType == 'JMP') or (myType == 'BEQ')):
        return 1
    elif(myType == 'ADD'):
        return 2
    elif(myType == 'MULT'):
        return 10
    else:
        return -1
def fillRS(rs, instruction, instructionType, pc, cycle):        
    
    rs['cycle'] = cycle
    rs['exec'] = -1
    ROB[tail[0]]['PC'] = pc
    if((instructionType == 'ADD') or (instructionType == 'NAND') or (instructionType == 'MULT')):
        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0] 
        if(RF[instruction[2]][0] == -1):
            rs['Vj'] = RF[instruction[2]][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF[instruction[2]][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF[instruction[2]][0]
            else:
                rs['Vj'] = ROB[RF[instruction[2]][0]]['Value']
                rs['Qj'] = -1
        
        
        if(instruction[0] != 'ADDI'):
            if(RF[instruction[3]][0] == -1):
                rs['Vk'] = RF[instruction[3]][1]
                rs['Qk'] = -1
            
            else:
                if(ROB[RF[instruction[3]][0]]['Ready'] == 'N'):
                    rs['Vk'] = 0
                    rs['Qk'] = RF[instruction[3]][0]
                else:
                    rs['Vk'] = ROB[RF[instruction[3]][0]]['Value']
                    rs['Qk'] = -1
        
        else:
            rs['Vk'] = instruction[3]
            rs['Qk'] = -1
            
        
        RF[instruction[1]][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8
        
        
    elif (instructionType == 'BEQ'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = -1
        ROB[tail[0]]['Ready'] = 'N'
        rs['Dest'] = tail[0]
        
        if(RF[instruction[1]][0] == -1):
            rs['Vj'] = RF[instruction[1]][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF[instruction[1]][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF[instruction[1]][0]
            else:
                rs['Vj'] = ROB[RF[instruction[1]][0]]['Value']
                rs['Qj'] = -1
        
        if(RF[instruction[2]][0] == -1):
            rs['Vk'] = RF[instruction[2]][1]
            rs['Qk'] = -1
        else:
            if(ROB[RF[instruction[2]][0]]['Ready'] == 'N'):
                rs['Vk'] = 0
                rs['Qk'] = RF[instruction[2]][0]
            else:
                rs['Vk'] = ROB[RF[instruction[2]][0]]['Value']
                rs['Qk'] = -1
            
        rs['A'] = instruction[3]
        tail[0] = (tail[0] + 1) % 8

    elif (instructionType == 'LW'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0]
        if(RF[instruction[2]][0] == -1):
            rs['Vj'] = RF[instruction[2]][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF[instruction[2]][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF[instruction[2]][0]
            else:
                rs['Vj'] = ROB[RF[instruction[2]][0]]['Value']
                rs['Qj'] = -1
        
        
        rs['Qk'] = -1
        rs['A'] = instruction[3]
        RF[instruction[1]][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8 #from 0 to 7
    

    elif (instructionType == 'SW'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = -1 #initialize to be -1 until execution ends
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0]
        
        if(RF[instruction[1]][0] == -1):
            rs['Vj'] = RF[instruction[1]][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF[instruction[1]][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF[instruction[1]][0]
            else:
                rs['Vj'] = ROB[RF[instruction[1]][0]]['Value']
                rs['Qj'] = -1
        
        if(RF[instruction[2]][0] == -1):
            rs['Vk'] = RF[instruction[2]][1]
            rs['Qk'] = -1
        
        else:
            if(ROB[RF[instruction[2]][0]]['Ready'] == 'N'):
                rs['Vk'] = 0
                rs['Qk'] = RF[instruction[2]][0]
            else:
                rs['Vk'] = ROB[RF[instruction[2]][0]]['Value']
                rs['Qk'] = -1
            
            
        rs['A'] = instruction[3]
        tail[0] = (tail[0] + 1) % 8 #from 0 to 7



    elif (instruction[0] == 'JMP'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = -1 #initialize to be -1 until execution ends
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0]
        
        rs['Qj'] = -1
        rs['Qk'] = -1
        rs['A'] = instruction[1] + pc + 1
        tail[0] = (tail[0] + 1) % 8 #from 0 to 7


    elif (instruction[0] == 'RET'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = -1 #initialize to be -1 until execution ends
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0]
        
        if(RF['R1'][0] == -1):
            rs['Vj'] = RF['R1'][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF['R1'][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF['R1'][0]
            else:
                rs['Vj'] = ROB[RF['R1'][0]]['Value']
                rs['Qj'] = -1
            
        rs['Qk'] = -1
        
        tail[0] = (tail[0] + 1) % 8 #from 0 to 7



    elif (instruction[0] == 'JALR'):

        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['Dest'] = 'R1'
        ROB[tail[0]]['Ready'] = 'N'
        
        rs['Dest'] = tail[0]
        
        if(RF[instruction[1]][0] == -1):
            rs['Vj'] = RF[instruction[1]][1]
            rs['Qj'] = -1
        
        else:
            if(ROB[RF[instruction[1]][0]]['Ready'] == 'N'):
                rs['Vj'] = 0
                rs['Qj'] = RF[instruction[1]][0]
            else:
                rs['Vj'] = ROB[RF[instruction[1]][0]]['Value']
                rs['Qj'] = -1
            
        rs['Qk'] = -1
        
        rs['A'] = pc + 1
        RF['R1'][0] = tail[0]
        tail[0] = (tail[0] + 1) % 8 #from 0 to 7
    


def decodeInstructionType(op):
    # if it is arithmetic
    if((op =='ADD' ) or (op == 'SUB') or (op == 'ADDI')):
        return 'ADD'
    
    # if it is a branch
    if((op == 'JMP') or (op == 'JALR') or (op == 'RET')):
        return 'JMP'
    
    # if it is anything else
    else:
        return op

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
            
            if(parts[0] == 'ADDI') or (parts[0] == 'BEQ') or (parts[0] == 'LW') or (parts[0] == 'SW'):
                thisInstruction.append(int(parts[3]))
            else:
                thisInstruction.append((parts[3]))
            
            instructions.append(thisInstruction)
        elif(len(parts) == 2):
            thisInstruction = []
            thisInstruction.append(parts[0])
            if(parts[0] == 'JMP'):
                thisInstruction.append(int(parts[1]))
            else:
                thisInstruction.append((parts[1]))
            instructions.append(thisInstruction)
        else:
            thisInstruction = []
            thisInstruction.append(parts[0])
            instructions.append(thisInstruction)
            
    
def writeUsingBus(result, ROBNumber):
    for key, value in RS.items():
        for rs in value:
            if(rs['Qj'] == ROBNumber):
                rs['Vj'] = result
                rs['Qj'] = - 1
            
            if(rs['Qk'] == ROBNumber):
                rs['Vk'] = result
                rs['Qk'] = - 1
        


branchMispredictions = 0
branchCounter = 0
instructionCounter = 0

readDataFromFile('datamem.txt')
stall = []
stall.append(0)
    
readInstructionsFromFile(instructions, 'sample.txt')    
while (usedROB != 0) or (pc < len(instructions)):
    
    if(pc < len(instructions)):
        # firstly, handle issuing
        instruction1 = instructions[pc]
        instruction1Type = decodeInstructionType(instruction1[0])
        #to do: if inst1 is a JMP, then fetch inst2 from prediction instead of pc+1
            
        instruction1Issued = 0
        instruction2Issued = 0
        
        if((usedROB < 8) and not(stall[0])): #we have enough space in ROB
            for rs in RS[instruction1Type]:
                if(rs['BUSY'] == 'N'):
                    instruction1Issued = 1
                    usedROB += 1
                    fillRS(rs, instruction1, instruction1Type, pc, cycle)
                    if(instruction1Type == 'JMP'):
                        stall[0] = 1
                    elif(instruction1Type == 'BEQ'):
                        if(instruction1[3] < 0):
                            pc = pc + 1 + instruction1[3]
                        else:
                            pc = pc + 1
                    else:
                        pc = pc + 1
                    break
            
            if(pc < len(instructions)):
                instruction2 = instructions[pc]
                instruction2Type = decodeInstructionType(instruction2[0])
                
                if((usedROB < 8) and instruction1Issued and not (stall[0])):
                    for rs in RS[instruction2Type]:
                        if(rs['BUSY'] == 'N'):
                            fillRS(rs, instruction2, instruction2Type, pc, cycle)
                            instruction2Issued = 1;
                            usedROB += 1
                            if(instruction2Type == 'JMP'):
                                stall[0] = 1
                            elif(instruction2Type == 'BEQ'):
                                if(instruction2[3] < 0):
                                    pc = pc + 1 + instruction2[3]
                                else:
                                    pc = pc + 1
                            else:
                                pc = pc + 1
                            break
                        
                        
    # secondly, handle committing:
    
    first = 1
    second = 0
    for i in range(2):
        if first or second:
            firstCommit = ROB[head[0]]
            if(firstCommit['Ready'] == 'Y'):
                first = 0
                second = 1
                if((firstCommit['Type'] == 'LW') or (firstCommit['Type'] == 'ADD') or (firstCommit['Type'] == 'SUB') or (firstCommit['Type'] == 'ADDI') or (firstCommit['Type'] == 'NAND') or (firstCommit['Type'] == 'MULT')):
                    if(RF[firstCommit['Dest']][0] == head[0]):
                        RF[firstCommit['Dest']][0] = -1
                        RF[firstCommit['Dest']][1] = firstCommit['Value']
                    usedROB -= 1
                    RF[firstCommit['Dest']][1] = firstCommit['Value']
                       
                elif(firstCommit['Type'] == 'SW'):
                   dataMemory[firstCommit['Dest']] = firstCommit['Value']
                   usedROB -= 1
                   
                elif(firstCommit['Type'] == 'JALR'):
                        
                    RF['R1'][0] = -1
                    RF['R1'][1] = firstCommit['Value']
                    pc = firstCommit['Dest']
                    stall[0] = 0
                    usedROB -= 1
                
                elif(firstCommit['Type'] == 'RET'):
                        
                    pc = firstCommit['Dest']
                    stall[0] = 0
                    usedROB -= 1
                    
                    
                elif(firstCommit['Type'] == 'JMP'):
                    
                        pc = firstCommit['Dest']
                        stall[0] = 0
                        usedROB -= 1
                        
                elif(firstCommit['Type'] == 'BEQ'):
                    # Update Value in writing: if we need to flush then Value = 1
                    branchCounter += 1
                    if(firstCommit['Value'] == 0): # wrong prediction
                       # we need to flush the ROB
                       pc = firstCommit['Dest']
                       clearRF_RS_ROB()
                       tail[0] = (head[0] + 1) % 8
                       usedROB = 0
                       branchMispredictions += 1
                       stall[0] = 0
                    else:
                       usedROB -= 1
                           
                firstCommit['Ready'] = 'N'
                head[0] = (head[0] + 1) % 8
                instructionCounter += 1
                
   
    
    
    # writing stage
    written = 0
    for key,value in RS.items():
        for rs in value:
            if ((rs['exec'] == 0) and (written < 2)):
                myOp = rs['op']
                if(myOp == 'ADD') or (myOp == 'ADDI'):
                    result = rs['Vj'] + rs['Vk']
                    ROB[rs['Dest']]['Value'] = result
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    written += 1
                    writeUsingBus(result, rs['Dest'])
                
                elif(myOp == 'SUB'):
                    result = rs['Vj'] - rs['Vk']
                    ROB[rs['Dest']]['Value'] = result
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    written += 1
                    writeUsingBus(result, rs['Dest'])
                    
                elif(myOp == 'MULT'):
                    result = rs['Vj'] * rs['Vk']
                    ROB[rs['Dest']]['Value'] = result
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    written += 1
                    writeUsingBus(result, rs['Dest'])
                    
                elif(myOp == 'NAND'):
                    result = not(rs['Vj'] and rs['Vk'])
                    ROB[rs['Dest']]['Value'] = result
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    written += 1
                    writeUsingBus(result, rs['Dest'])
                
                elif(myOp == 'LW'):
                    result = dataMemory[rs['A']]
                    ROB[rs['Dest']]['Value'] = result
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    written += 1
                    writeUsingBus(result, rs['Dest'])
                
                elif(myOp == 'SW'):
                    
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    ROB[rs['Dest']]['Value'] =  rs['Vj']
                    ROB[rs['Dest']]['Dest'] = rs['A']
                    written += 1
                    
                elif(myOp == 'JMP'):
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    #we set the value in the ROB to the address that we want to jump to
                    ROB[rs['Dest']]['Dest'] =  rs['A']
                    written += 1
                
                elif(myOp == 'RET'):
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    ROB[rs['Dest']]['Dest'] =  rs['Vj']
                    written += 1
                
                elif(myOp == 'JALR'):
                    result = rs['A']
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    ROB[rs['Dest']]['Dest'] =  rs['Vj']
                    ROB[rs['Dest']]['Value'] =  rs['A']
                    writeUsingBus(result, rs['Dest'])
                    written += 1
                
                elif(myOp == 'BEQ'):
                    written += 1
                    ROB[rs['Dest']]['Ready'] = 'Y'
                    branchPC = ROB[rs['Dest']]['PC']
                    if((rs['Vj'] == rs['Vk'])):
                        ROB[rs['Dest']]['Dest'] = branchPC + rs['A'] + 1
                    else:
                        ROB[rs['Dest']]['Dest'] = branchPC + 1
                    if((rs['Vj'] == rs['Vk']) and (rs['A'] < 0)) or ((rs['Vj'] != rs['Vk']) and (rs['A'] > 0)):
                        ROB[rs['Dest']]['Value'] = 1
                    else:
                        ROB[rs['Dest']]['Value'] = 0
                        
                rs['exec'] = -1
                rs['BUSY'] =  'N'
                rs['op'] =  'NULL'
                rs['Vj'] = 0
                rs['Vk'] = 0
                rs['Qj'] = -1
                rs['Qk'] = -1
                rs['Dest'] = -1
                rs['A'] = 0
    
    
    
    #start executing instructions with ready operands
    for key,value in RS.items():
        for rs in value:
            if((rs['Qj'] == -1) and (rs['Qk'] == -1) and (rs['exec'] < 0) and rs['BUSY'] == 'Y'):
                
                myType = decodeInstructionType(rs['op'])
                rs['exec'] = getDelay(myType)
                if(rs['op'] == 'LW'):
                    rs['A'] += rs['Vj']
                    
                if(rs['op'] == 'SW'):
                    rs['A'] += rs['Vk']
                    
            elif(rs['exec'] != 0):
                rs['exec'] -= 1
            
    cycle += 1
    
    
# Report the results after commiting all instructions
print ('Total Clock Cycles = ', cycle)
print ('Number of Instructions = ', instructionCounter)
print ('IPC = ', instructionCounter/cycle)
print ('Branch Instructions = ', branchCounter)
print ('Branch Mispredictions = ', branchMispredictions)
if(branchCounter > 0):
    print ('Branch misprediction rate = ', branchMispredictions/branchCounter)
else:
    print ('Branch misprediction rate = ', 0)