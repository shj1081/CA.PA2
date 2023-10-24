# write a code that convert integer to 32 bit 2's complement hexadecimal (8 characters wide)

def int_to_hex(integer):
    if integer < 0:
        return format((1 << 32) + integer, "08x")
    else:
        return format(integer, "08x")
    

print (int_to_hex(-32))