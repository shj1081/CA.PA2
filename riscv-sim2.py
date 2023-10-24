import sys

"""
bin file to 4 bytes binary string list
"""
def read_binary_file(file_path):
    binary_data = []
    with open(file_path, "rb") as binary_file:
        while True:
            chunk = binary_file.read(4)  # Read 4 bytes (32 bits) at a time
            if not chunk:
                break

            # Convert the 32 bits into a binary string (little endian to big endian)
            value = int.from_bytes(chunk, byteorder="little", signed=False)
            binary_value = format(value, "032b")
            binary_data.append(binary_value)

    return binary_data

"""
converts a binary string to a signed integer (2's complement)
"""
def imm_to_int(binary_str):
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
    return register_list[register_number]

def write_register(register_number, value):
    register_list[register_number] = value


"""
access memory
"""
def read_memory(address):
    return data_memory_list[address]

def write_memory(address, value):
    data_memory_list[address] = value


"""
convert 4 byte binary string to instruction
"""
def binary_to_instruction(binary_str):
    opcode = binary_str[25:32]

    # R-Type Instructions
    if opcode == "0110011":
        funct3 = binary_str[17:20]
        funct7 = binary_str[0:7]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]

        if funct3 == "000" and funct7 == "0000000":
            return f"add x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "000" and funct7 == "0100000":
            return f"sub x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "001" and funct7 == "0000000":
            return f"sll x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "010" and funct7 == "0000000":
            return f"slt x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "100" and funct7 == "0000000":
            return f"xor x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "101" and funct7 == "0000000":
            return f"srl x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "101" and funct7 == "0100000":
            return f"sra x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "110" and funct7 == "0000000":
            return f"or x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"
        elif funct3 == "111" and funct7 == "0000000":
            return f"and x{int(rd, 2)}, x{int(rs1, 2)}, x{int(rs2, 2)}"

    # I-Type Instructions
    elif opcode in {"0010011", "0000011", "1100111"}:
        funct3 = binary_str[17:20]
        rd = binary_str[20:25]
        rs1 = binary_str[12:17]
        imm = binary_str[0:12]

        if opcode == "0010011":
            if funct3 == "000":
                return f"addi x{int(rd, 2)}, x{int(rs1, 2)}, {imm_to_int(imm)}"
            elif funct3 == "010":
                return f"slti x{int(rd, 2)}, x{int(rs1, 2)}, {imm_to_int(imm)}"
            elif funct3 == "100":
                return f"xori x{int(rd, 2)}, x{int(rs1, 2)}, {imm_to_int(imm)}"
            elif funct3 == "110":
                return f"ori x{int(rd, 2)}, x{int(rs1, 2)}, {imm_to_int(imm)}"
            elif funct3 == "111":
                return f"andi x{int(rd, 2)}, x{int(rs1, 2)}, {imm_to_int(imm)}"
            elif funct3 == "001" and imm[0:7] == "0000000":
                return f"slli x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:],2)}"
            elif funct3 == "101" and imm[0:7] == "0000000":
                return f"srli x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:],2)}"
            elif funct3 == "101" and imm[0:7] == "0100000":
                return f"srai x{int(rd, 2)}, x{int(rs1, 2)}, {int(imm[7:],2)}"

        elif opcode == "0000011":
            if funct3 == "010":
                return f"lw x{int(rd, 2)}, {imm_to_int(imm)}(x{int(rs1, 2)})"

        elif opcode == "1100111" and funct3 == "000":
            return f"jalr x{int(rd, 2)}, {imm_to_int(imm)}(x{int(rs1, 2)})"

    # S-Type Instructions
    elif opcode == "0100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0:7] + binary_str[20:25]
        
        if funct3 == "010":
            return f"sw x{int(rs2, 2)}, {imm_to_int(imm)}(x{int(rs1, 2)})"

    # SB-Type Instructions
    elif opcode == "1100011":
        funct3 = binary_str[17:20]
        rs1 = binary_str[12:17]
        rs2 = binary_str[7:12]
        imm = binary_str[0] + binary_str[24] + binary_str[1:7] + binary_str[20:24] + "0"

        if funct3 == "000":
            return f"beq x{int(rs1, 2)}, x{int(rs2, 2)}, {imm_to_int(imm)}"
        elif funct3 == "001":
            return f"bne x{int(rs1, 2)}, x{int(rs2, 2)}, {imm_to_int(imm)}"
        elif funct3 == "100":
            return f"blt x{int(rs1, 2)}, x{int(rs2, 2)}, {imm_to_int(imm)}"
        elif funct3 == "101":
            return f"bge x{int(rs1, 2)}, x{int(rs2, 2)}, {imm_to_int(imm)}"

    # U-Type Instructions
    elif opcode in {"0110111", "0010111"}:
        rd = binary_str[20:25]
        imm = binary_str[0:20] + "000000000000"

        if opcode == "0110111":
            return f"lui x{int(rd, 2)}, {imm_to_int(imm)}"
        elif opcode == "0010111":
            return f"auipc x{int(rd, 2)}, {imm_to_int(imm)}"

    # UJ-type Instructions
    elif opcode == "1101111":
        rd = binary_str[20:25]
        imm = (
            binary_str[0] + binary_str[12:20] + binary_str[11] + binary_str[1:11] + "0"
        )
        return f"jal x{int(rd, 2)}, {imm_to_int(imm)}"


"""
function to execute instruction
"""
def execute_instruction(instruction_list, data_list, instruction_number):
    pass


"""
print register values
"""
def print_register():
    pass


"""
main
"""
register_list= [0 for i in range(32)]
data_memory_list = [0 for i in range(64 * 1024)] # only for data not instruction
program_counter = 0

# load binary instrunction to instruction_list
binary_instructions_path = sys.argv[1]
instruction_list = read_binary_file(binary_instructions_path)

if len(sys.argv) == 3:
    instruction_number = int(sys.argv[2])
    
elif len(sys.argv) == 4:
    binary_data_path = sys.argv[2]
    instruction_number = int(sys.argv[3])

    # load data to data_memory_list
    data_list = read_binary_file(binary_data_path)
    data_memory_list[0:len(data_list)] = data_list
    
