

def dec_to_bin(d):
    if d >= 0:
        return (8 - len(bin(d)[2:]))*'0'+ bin(d)[2:]
    else:
        x = (8 - len(bin(-d)[2:]))*'0' + bin(-d)[2:]
        a = x.replace('1', '2').replace('0' , '3')
        x = a.replace('2', '0').replace('3' , '1')
        b = int(x, 2) + 1 
        return bin(b)[2:]

print(dec_to_bin(47))
print(dec_to_bin(-109))
print(dec_to_bin(-67))
print(dec_to_bin(81))
