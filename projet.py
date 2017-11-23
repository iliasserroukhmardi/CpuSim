program = open("programme.txt", "r")

memoryFile = open("initMemoire.txt", "r")

instructions = program.readlines()
m = memoryFile.readlines()


""" R[:4] ===> work registers  
    R[4]  ===> instruction register 
    R[5]  ===> program counter 
    R[6]  ===> state register  """
R = ['00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000']
running = True


def bin_to_dec(b):
    """returns decimal representation of a 2's compliment binary number"""
    if b[0] == '0':
        return int(b, 2)
    else:
        a = b.replace('1', '2').replace('0' , '3')
        b = a.replace('2', '0').replace('3' , '1')
        return -1 *(int(b,2) + 1)

def dec_to_bin(d):
    """returns 2's compliment binary representation of a decimal number"""
    if d >= 0:
        return (8 - len(bin(d)[2:]))*'0'+ bin(d)[2:]
    else:
        x = (8 - len(bin(-d)[2:]))*'0' + bin(-d)[2:]
        a = x.replace('1', '2').replace('0' , '3')
        x = a.replace('2', '0').replace('3' , '1')
        b = int(x, 2) + 1
        return bin(b)[2:]


memory = {}
for i in m:
    i = i.rstrip().replace(" ", "").split(":")
    memory[dec_to_bin(int(i[0]))]= dec_to_bin(int(i[1]))



def WRL(data):
    """ write data to operand of register R0 
    global R0 
    R0 = R0[:4] + data"""
    R[0] = R[0][:4] + data

def WRH(data):
    """ write data to opcode of register R0 """
    R[0] = data + R[0][4:]
    

def MOV(data):
    """ data = abcd 
        register_A = R_(ab) and register_B =R(cd)"""
    R[int(data[:2],2)] = R[int(data[2:],2)]
    
def STR(data):
    """ data = abcd """
    memory[R[int(data[2:],2)]] = R[int(data[:2],2)]

def RD(data):
    "change value of R[int(data[:2],2)] with the value found in memory addres int(R[int(data[2:],2)], 2)"

    """WHAT IF THE MEMORY ISNT SPECIFIED IN THE initMemoirel.txt doc do we give it a value of 0 """
    R[int(data[:2],2)] = memory.get(R[int(data[2:],2)], '00000000')


def ADD(data):
    """add registers """
    a = bin_to_dec(R[int(data[:2],2)])
    b = bin_to_dec(R[int(data[2:],2)])
    R[int(data[:2],2)] = dec_to_bin(a + b)
    if a + b == 0:
        R[6] = '00000001'

def INV(data):
    """ multiply by -1 the value ..."""
    a = bin_to_dec(R[int(data[2:],2)]) * -1
    R[int(data[2:],2)] = dec_to_bin(a)

def JP(data):
    a = bin_to_dec(R[5]) + bin_to_dec(data)
    R[5] = dec_to_bin(a)

def JZ(data):
    if R[6] == '00000001':
        JP(data)

def JNZ(data):
    if R[6] == '00000000':
        JP(data)

def END(data = '0000'):
    global running 
    running = False


opcodes = {'0000':WRL, '0001':WRH, '0010':MOV, '0011':STR, '0100':RD, '0101':ADD,
     '0110':INV, '0111':JP, '1000':JZ, '1001':JNZ, '1010':END}



def printRegisters():
    print("Registers ==>    R0: " + R[0] + " "*5 + "R1: " + R[1])
    print("                 R2: " + R[2] + " "*5 + "R3: " + R[3])
    print("                 IR: " + R[4] + " "*5 + "PC: " + R[5] + "\n")

def printMemory():
    print("\nVALUES IN MEMORY WHICH ARE NOT EMPTY \n   ADDRESS" + 10*" "+ "VALUE" ) 
    for i in memory:
        print(i +" ("+str(bin_to_dec(i))+"): " + memory[i] +" ("+str(bin_to_dec(memory[i]))+")")
    print(" \n")

def inputCheck():
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
                u = input("PRESS 1: CONTINUE \n")
            else:
                print("INVALID INPUT")
                inputCheck()
    except (NameError, SyntaxError):
        print("INVALID INPUT")
        inputCheck()







iset=[]
for i in instructions:
    iset.append(i.strip())

def run():
    i = 0
    phase = ("FETCH", "DECODE", "EXECUTE")
    while running:
        #Fetch
        print("Cycle: " + str(i) + " ==> " + phase[0])
        printRegisters()
        R[4] = iset[bin_to_dec(R[5])]
        R[5] = dec_to_bin(bin_to_dec(R[5]) + 1)
        inputCheck()
        #Decode
        print("Cycle: " + str(i) + " ==> " + phase[1])
        opcodes[R[4][:4]](R[4][4:])
        #Execute
        

        i+=1



run()























