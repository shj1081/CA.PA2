import sys

"""
bin file to 4 bytes binary string list
"""


def read_binary_file_4byte(file_path):
    binary_data_list = []
    with open(file_path, "rb") as binary_file:
        while True:
            chunk = binary_file.read(4)  # Read 4 bytes (32 bits) at a time
            if not chunk:
                break

            # Convert the 32 bits into a binary string (little endian to big endian)
            value = int.from_bytes(
                chunk, byteorder="little", signed=False
            )  # machine code to int
            binary_value = format(value, "032b")  # int to binary string
            binary_data_list.append(binary_value)

    return binary_data_list


def read_binary_file_1byte(file_path):
    binary_data_list = []
    with open(file_path, "rb") as binary_file:
        while True:
            chunk = binary_file.read(1)  # Read 1 byte at a time
            if not chunk:
                break

            # Convert the byte into a binary string
            value = ord(chunk)  # machine code to ascii
            binary_value = format(value, "08b")  # ascii to binary string
            binary_data_list.append(binary_value)

    return binary_data_list


"""
converts an immediate (binary string) to a signed integer (2's complement)
"""


def binary_to_int(binary_str):
    # Check if it's a negative number (2's complement)
    if binary_str[0] == "1":
        inverted_str = "".join(["1" if bit == "0" else "0" for bit in binary_str])
        absolute_value = int(inverted_str, 2) + 1
        return -absolute_value
    else:
        return int(binary_str, 2)


"""
access register
"""


def read_register(register_number):
    if register_number == 0:  # (x0 = 0 always)
        return 0
    else:
        return register_list[register_number]


def write_register(register_number, value):
    if register_number != 0:  # (x0 = 0 always)
        register_list[register_number] = value


"""
get address
"""


def get_address(rs1, imm):
    return register_list[rs1] + imm


"""
access memory
"""


# read 4 byte integer from data memory
def read_memory(address):
    binary_str = ""
    for i in range(4):
        binary_str += data_memory_list[address + (3 - i)]
        decimal_value = binary_to_int(binary_str)
    return decimal_value


# write 4 byte integer to data memory
def write_memory(address, decimal_value):
    binary_str = format(decimal_value, "032b")
    for i in range(4):
        data_memory_list[address + (3 - i)] = binary_str[8 * i : 8 * (i + 1)]


"""
each instruction 
"""


def add_instruction(rd, rs1, rs2):
    write_register(rd, read_register(int(rs1, 2)) + read_register(int(rs2, 2)))


def sub_instruction(rd, rs1, rs2):
    write_register(rd, read_register(int(rs1, 2)) - read_register(int(rs2, 2)))


def sll_instruction(rd, rs1, rs2):
    write_register(
        rd, read_register(int(rs1, 2)) << read_register(int(rs2, 2) & 0b11111)
    )  # only for rs2's lower 5 bits


def slt_instruction(rd, rs1, rs2):
    if read_register(int(rs1, 2)) < read_register(int(rs2, 2)):
        write_register(rd, 1)
    else:
        write_register(rd, 0)


def xor_instruction(rd, rs1, rs2):
    write_register(rd, read_register(int(rs1, 2)) ^ read_register(int(rs2, 2)))


def srl_instruction(rd, rs1, rs2):
    pass


def sra_instruction(rd, rs1, rs2):
    write_register(
        rd, read_register(int(rs1, 2)) >> read_register(int(rs2, 2) & 0b11111)
    )  # only for rs2's lower 5 bits


def or_instruction(rd, rs1, rs2):
    write_register(rd, read_register(int(rs1, 2)) | read_register(int(rs2, 2)))


def and_instruction(rd, rs1, rs2):
    write_register(rd, read_register(int(rs1, 2)) & read_register(int(rs2, 2)))


def addi_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) + binary_to_int(imm))


def slti_instruction(rd, rs1, imm):
    if read_register(int(rs1, 2)) < binary_to_int(imm):
        write_register(rd, 1)
    else:
        write_register(rd, 0)


def xori_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) ^ binary_to_int(imm))


def ori_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) | binary_to_int(imm))


def andi_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) & binary_to_int(imm))


def slli_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) << int(imm, 2))


def srli_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) >> int(imm, 2))


def srai_instruction(rd, rs1, imm):
    write_register(rd, read_register(int(rs1, 2)) >> int(imm, 2))


def lw_instruction(rd, rs1, imm):
    write_register(rd, read_memory(get_address(int(rs1, 2), binary_to_int(imm))))
    # TODO : x20000000 case


def sw_instruction(rs1, rs2, imm):
    write_memory(
        get_address(int(rs1, 2), binary_to_int(imm)), read_register(int(rs2, 2))
    )
    # TODO : x20000000 case


def beq_instruction(rs1, rs2, imm):
    if read_register(int(rs1, 2)) == read_register(int(rs2, 2)):
        program_counter += binary_to_int(imm)
        return
    else:
        pass


def bne_instruction(rs1, rs2, imm):
    if read_register(int(rs1, 2)) != read_register(int(rs2, 2)):
        program_counter += binary_to_int(imm)
        return
    else:
        pass


def blt_instruction(rs1, rs2, imm):
    if read_register(int(rs1, 2)) < read_register(int(rs2, 2)):
        program_counter += binary_to_int(imm)
        return
    else:
        pass


def bge_instruction(rs1, rs2, imm):
    if read_register(int(rs1, 2)) >= read_register(int(rs2, 2)):
        program_counter += binary_to_int(imm)
        return
    else:
        pass


def lui_instruction(rd, imm):
    write_register(rd, binary_to_int(imm) << 3)


def auipc_instruction(rd, imm):
    write_register(rd, (program_counter * 4) + (binary_to_int(imm) << 3))


def jal_instruction(rd, imm):
    write_register(rd, program_counter + 1)
    program_counter += binary_to_int(imm) / 4
    return


def jalr_instruction(rd, rs1, imm):
    write_register(rd, program_counter + 1)
    program_counter = (read_register(int(rs1, 2)) + binary_to_int(imm)) / 4
    return
    # TODO : need to check if it is correct


"""
execute binary instruction
"""


def execute_binary_instruction(binary_str):
    # global variables
    global program_counter
    global register_list
    global data_memory_list

    # get opcode for determining instruction
    opcode = binary_str[25:32]

    # R-Type Instructions
    if opcode == "0110011":
        funct3 = binary_str[17:20]
        funct7 = binary_str[0:7]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]

        if funct3 == "000" and funct7 == "0000000":
            add_instruction(rd, rs1, rs2)
        elif funct3 == "000" and funct7 == "0100000":
            sub_instruction(rd, rs1, rs2)
        elif funct3 == "001" and funct7 == "0000000":
            sll_instruction(rd, rs1, rs2)
        elif funct3 == "010" and funct7 == "0000000":
            slt_instruction(rd, rs1, rs2)
        elif funct3 == "100" and funct7 == "0000000":
            xor_instruction(rd, rs1, rs2)
        elif funct3 == "101" and funct7 == "0000000":
            srl_instruction(rd, rs1, rs2)
        elif funct3 == "101" and funct7 == "0100000":
            sra_instruction(rd, rs1, rs2)
        elif funct3 == "110" and funct7 == "0000000":
            or_instruction(rd, rs1, rs2)
        elif funct3 == "111" and funct7 == "0000000":
            and_instruction(rd, rs1, rs2)

    # I-Type Instructions
    elif opcode in {"0010011", "0000011", "1100111"}:
        funct3 = binary_str[17:20]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        imm = binary_str[0:12]

        if opcode == "0010011":
            if funct3 == "000":
                addi_instruction(rd, rs1, imm)
            elif funct3 == "010":
                slti_instruction(rd, rs1, imm)
            elif funct3 == "100":
                xori_instruction(rd, rs1, imm)
            elif funct3 == "110":
                ori_instruction(rd, rs1, imm)
            elif funct3 == "111":
                andi_instruction(rd, rs1, imm)
            elif funct3 == "001" and imm[0:7] == "0000000":
                slli_instruction(rd, rs1, imm) 
            elif funct3 == "101" and imm[0:7] == "0000000":
                srli_instruction(rd, rs1, imm)
            elif funct3 == "101" and imm[0:7] == "0100000":
                srai_instruction(rd, rs1, imm)

        elif opcode == "0000011":
            if funct3 == "010":
                lw_instruction(rd, rs1, imm)

        elif opcode == "1100111" and funct3 == "000":
            jalr_instruction(rd, rs1, imm)

    # S-Type Instructions
    elif opcode == "0100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0:7] + binary_str[20:25]

        if funct3 == "010":
            sw_instruction(rs1, rs2, imm)

    # SB-Type Instructions
    elif opcode == "1100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0] + binary_str[24] + binary_str[1:7] + binary_str[20:24] + "0"

        if funct3 == "000":
            beq_instruction(rs1, rs2, imm)
        elif funct3 == "001":
            bne_instruction(rs1, rs2, imm)
        elif funct3 == "100":
            blt_instruction(rs1, rs2, imm)
        elif funct3 == "101":
            bge_instruction(rs1, rs2, imm)

    # U-Type Instructions
    elif opcode in {"0110111", "0010111"}:
        rd = binary_str[20:25]
        imm = binary_str[0:20]

        if opcode == "0110111":
            return f"lui x{int(rd, 2)}, {binary_to_int(imm)}"
        elif opcode == "0010111":
            return f"auipc x{int(rd, 2)}, {binary_to_int(imm)}"

    # UJ-type Instructions
    elif opcode == "1101111":
        rd = binary_str[20:25]
        imm = (
            binary_str[0] + binary_str[12:20] + binary_str[11] + binary_str[1:11] + "0"
        )
        jal_instruction(rd, imm)

    program_counter += 1


"""
convert integer to 32 bit 2's complement hexadecimal
"""


def int_to_hex(integer):
    if integer < 0:
        return format((1 << 32) + integer, "08x")  # 2's complement property
    else:
        return format(integer, "08x")


"""
print register values
"""


def print_register(register_list):
    for i in range(32):
        print(f"x{i}: {int_to_hex(register_list[i])}")


"""
main
"""


register_list = [0 for i in range(32)]
data_memory_list = [
    "11111111" for i in range(64 * 1024)  # 64KB = 64 * 1024 Byte
]  # only for data not instruction, initialize with "11111111"(0xff)
program_counter = 0

# load binary instrunction to instruction_list (1 element = 4 byte)
binary_instructions_path = sys.argv[1]
instruction_list = read_binary_file_4byte(binary_instructions_path)

if len(sys.argv) == 3:
    instruction_number = int(sys.argv[2])

elif len(sys.argv) == 4:
    binary_data_path = sys.argv[2]
    instruction_number = int(sys.argv[3])

    # load data to data_memory_list (1 element = 1 byte)
    binary_data_list = read_binary_file_1byte(binary_data_path)
    data_memory_list[0 : len(binary_data_list)] = binary_data_list

for i in range(instruction_number):
    execute_binary_instruction(instruction_list[i])

print_register(register_list)
