program = open("programme.txt", "r")
instructions = program.readlines()

""" R[:4] ===> work registers  
    R[4]  ===> instruction register 
    R[5]  ===> program counter 
    R[6]  ===> state register  """
R = ['00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000']




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




def WRL(data):
    """ write data to operand of register R0 
    global R0 
    R0 = R0[:4] + data"""
    R[0] = R[0][:4] + data

def WRH(data):
    """ write data to opcode of register R0 """
    global R0
    R[0] = data + R[0][4:]
    

def MOV(data):
    """ data = abcd 
        register_A = R_(ab) and register_B =R(cd)"""
    R[int(data[2:],2)] = R[int(data[:2],2)]
    
def STR(data):
    """ data = abcd """
    instructions[int(R[int(data[2:], 2)], 2)] = R[int(data[:2], 2)]

def RD(data):
    "change value of R[int(data[:2],2)] with the value found in memory addres int(R[int(data[2:],2)], 2)"
    R[int(data[:2],2)] = instructions[int(R[int(data[2:],2)], 2)-1]


def ADD(data):
    """add registers """
    a = bin_to_dec(R[int(data[:2],2)])
    b = bin_to_dec(R[int(data[2:],2)])
    R[int(data[:2],2)] = dec_to_bin(a + b)
    if a + b == 0:
        R[6] = '00000001'
    else:
        R[6] = '00000000'

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

