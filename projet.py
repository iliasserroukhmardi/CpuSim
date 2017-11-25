import sys
from numpy import binary_repr

arg_A =  "initMemoire.txt"  #sys.argv[0]
arg_B =  "programme.txt" #sys.argv[1]

memoryFile = open(arg_A, "r")
programFile = open(arg_B, "r")



###################################### USEFUL FUNCTIONS ######################################
def bin2dec(b):
    """
        Returns decimal representation of a 2's compliment binary number
    """
    if b[0] == '0':
        return int(b, 2)
    else:
        b = b.replace("1", "x").replace("0", "1").replace("x", "0") 
        return -1 * int(b,2) + 1

def dec2bin(d):
    """
        Returns 2's compliment binary representation of a decimal number
        (Written in this manner for symmetry with bin2dec)
    """   
    return binary_repr(d, width=8)


def printRegisters():
    """
        Prints the work registers, the instruction register and the program counter in a readable way
    """
    print("Registers ==>    R0: " + R[0][:4]+" "+R[0][4:] + " "*5 + "R1: " + R[1][:4]+" "+R[1][4:])
    print("                 R2: " + R[2][:4]+" "+R[2][4:] + " "*5 + "R3: " + R[3][:4]+" "+R[3][4:] + " "*5 + "ST: "+ R[6][-1])
    print("                 IR: " + R[4][:4]+" "+R[4][4:] + " "*5 + "PC: " + R[5][:4]+" "+R[5][4:] + "\n")


def printMemory():
    """
        Prints the Memory addresses which are not empty  in a readable way
    """
    print("\nVALUES IN MEMORY WHICH ARE NOT EMPTY \n   ADDRESS" + 10*" "+ "VALUE" ) 
    for i in Memory:
        print(i +" ("+str(bin2dec(i))+"): " + Memory[i] +" ("+str(bin2dec(Memory[i]))+")")
    print(" \n")


def inputCheck():
    """
        Prints the possible input options (what can the user see) in a readable way
        Also makes sure that only the right input is typed (1 or 2)
        For debugging purposes Ctr+c allows quitting the simulation
    """
    try:
        v = input("PRESS 1: CONTINUE \n" + 6*" " + "2: VIEW MEMORY \n")
        if type(v) != type(1):
            print("INVALID INPUT")
            inputCheck()
        else:
            if v == 1:
                pass
            elif v == 2:
                printMemory()
                inputCheck()
            else:
                print("INVALID INPUT")
                inputCheck()
    except (NameError, SyntaxError):
        print("INVALID INPUT")
        inputCheck()



###################  LOAD THE PROGRAM, THE MEMORY AND THE REGISTERS  ###########################

#Load the program as a list of instructions
InstrSet=[line.strip() for line in programFile]

"""
    Load the Memory as a dictionary where the Memory address is the key
    and the value is what is actually inside the Memory address
"""
Memory = {}
for i in memoryFile:
    i = i.rstrip().replace(" ", "").split(":")
    Memory[dec2bin(int(i[0]))] = dec2bin(int(i[1]))


""" 
    Create all the registers and store them iside a list
    R[0] to R[3] ===> the actual working registers  
    R[4]         ===> instruction register (IR)
    R[5]         ===> program counter      (PC)
    R[6]         ===> state register       (ST)
"""
R = ['00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000']


#Set the procesor to running when script is called
running = True
    

###################################### OPCODES (INSTRUCTIONS) ######################################

def WRL(AB):
    """ 
        Write AB to operand of register R0 
        (AB is a 4 bit binary number)
    """
    R[0] = R[0][:4] + AB

def WRH(AB):
    """ 
        Write AB to opecode of register R0 
        (AB is a 4 bit binary number)
    """
    R[0] = AB + R[0][4:]
    
def MOV(AB):
    """ 
        Copy the value of register B and paste it in register A
        (A and B are 2 bit binary numbers)
    """
    R[int(AB[:2],2)] = R[int(AB[2:],2)]
    
def STR(AB):
    """ 
        Write the value of register A into the Memory address given by 
        the value of register B
        (A and B are 2 bit binary numbers)
    """
    Memory[R[int(AB[2:],2)]] = R[int(AB[:2],2)]

def RD(AB):
    """
        Write the value of the Memory address given by register A to
        register B
        (A and B are 2 bit binary numbers)  
    """
    R[int(AB[:2],2)] = Memory.get(R[int(AB[2:],2)], '00000000')

def ADD(AB):
    """
        Write the sum of the values inside the registers A and B to 
        the register A
        If the sum equals 0, set the ST register equatl to 00000001
        (A and B are 2 bit binary numbers)
    """
    a = bin2dec(R[int(AB[:2],2)])
    b = bin2dec(R[int(AB[2:],2)])
    R[int(AB[:2],2)] = dec2bin(a + b)
    if a + b == 0:
        R[6] = '00000001'
    else:
        R[6] = '00000000'

def INV(AB):
    """ 
        Multiply by -1 the value of the register B
        (B is a 2 bit binary number, A is ignored)
    """
    a = bin2dec(R[int(AB[2:],2)]) * -1
    R[int(AB[2:],2)] = dec2bin(a)

def JP(AB):
    """ 
        Add to the PC register the value AB 
        (here AB is a number not a register)
    """
    a = bin2dec(R[5]) + bin2dec(AB)
    R[5] = dec2bin(a)

def JZ(AB):
    """ 
        Add to the PC register the value AB only if the value of ST is 0
        (here AB is a number not a register)
    """
    if R[6] == '00000001':
        JP(AB)

def JNZ(AB):
    """ 
        Add to the PC register the value AB only if the value of ST is 1
        (here AB is a number not a register)
    """
    if R[6] == '00000000':
        JP(AB)

def END(AB = '0000'):
    """
        End the execution 
        (AB is ignored)
    """
    global running 
    running = False

"""
    Store functions in a dictionary, where the keys are the actual opcodes and the 
    values are the functions
"""
opcodes = {'0000':WRL, '0001':WRH, '0010':MOV, '0011':STR, '0100':RD, '0101':ADD,
     '0110':INV, '0111':JP, '1000':JZ, '1001':JNZ, '1010':END}


###################################### Execute  ######################################

running = True
def run():
    i = 1
    while running:
        #Fetch
        print("Cycle: " + str(i) + " ==> " + "FETCH")
        printRegisters()
        inputCheck()
        R[4] = InstrSet[bin2dec(R[5])]
        #Decode
        R[5] = dec2bin(bin2dec(R[5]) + 1)
        print("Cycle: " + str(i) + " ==> " + "DECODE")
        printRegisters()
        inputCheck()
        #Execute
        print("Cycle: " + str(i) + " ==> " + "EXECUTE")
        printRegisters()
        print("Decoded Instruction: " + opcodes[R[4][:4]].__name__ + " " +R[4][4:])
        inputCheck()
        opcodes[R[4][:4]](R[4][4:])
        i += 1


run()

"""
def Fetch():
    R[4] = InstrSet[bin2dec(R[5])]
    R[5] = dec2bin(bin2dec(R[5]) + 1)

def Decode():
"""
