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
RS['ADD'][0][1] = 'Y'


dataMemory = [0] * 65536

RF = {}

#R2 is a register that is used by ROB1 and has the value of 25
RF['R0'] = [0,0]
RF['R1'] = [0,1]
RF['R2'] = [0,2]
RF['R3'] = [0,3]
RF['R4'] = [0,4]
RF['R5'] = [0,5]
RF['R6'] = [0,6]
RF['R7'] = [0,7]

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
head.append(1)
tail = []
tail.append(1)

instruction = ['ADD', 'R2', 'R2', 'R3']
instructions = [instruction.copy() for i in range(5)]

pc = 0
cycle = 0



def fillRS(rs, instruction):
    if(instruction[0] == 'ADD'):
        rs['BUSY'] = 'Y'
        rs['op'] = instruction[0]
        ROB[tail[0]]['Type'] = instruction[0]
        ROB[tail[0]]['DEST'] = instruction[1]
        ROB[tail[0]]['Ready'] = 'N'
        RF[instruction[1]][0] = tail
        
        tail[0] = (tail[0] + 1)%8
        
        rs['DEST'] = RF[instruction[1]][0]
        if(RF[instruction[2]] == 0):
            rs['Vj'] = RF[instruction[2]][1]
            rs['Qj'] = 0
        
        else:
            rs['Vj'] = 0
            rs['Qj'] = RF[instruction[2]][0]
        
        
        if(RF[instruction[3]] == 0):
            rs['Vk'] = RF[instruction[3]][1]
            rs['Qk'] = 0
        
        else:
            rs['Vk'] = 0
            rs['Qk'] = RF[instruction[3]][0]
        
while pc<4:
    instruction1 = instructions[pc]
    
    #to do: if inst1 is a JMP, then fetch inst2 from prediction instead of pc+1
    instruction2 = instructions[pc + 1]
    instruction1Issued = 0
    instruction2Issued = 0
    
    if(usedROB < 8): #we have enough space in ROB
        
        
        for rs in RS[instruction1[0]]:
            if(rs['BUSY'] == 'N'):
                instruction1Issued = 1
                usedROB += 1
                fillRS(rs, instruction1)
                break
        
        if(usedROB < 8) and instruction1Issued:
            
            for rs in RS[instruction2[0]]:
                if(rs['BUSY'] == 'N'):
#                    fillRS(rs, instruction2)
                    instruction2Issued
                    usedROB += 1
                    break;
    
    
    
    if(instruction2Issued):
        pc += 2
    elif(instruction1Issued):
        pc += 1
        
    cycle += 1
    print(cycle)
    
    

        
        
        