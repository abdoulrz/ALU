import math

class CPU:
    def __init__(self):
        # Registers: A fixed list of 4 memory slots (like R0, R1, R2, R3)
        self.registers = [0] * 4 
        # Cache: A dictionary to store results of operations: {(op, val1, val2): result}
        self.cache = {}

    def load(self, reg_index, value):
        """Loads a value into a specific register."""
        if 0 <= reg_index < len(self.registers):
            self.registers[reg_index] = value
        else:
            raise ValueError("Invalid register index")

    def get_register(self, reg_index):
        """Returns the value of a register."""
        if 0 <= reg_index < len(self.registers):
            return self.registers[reg_index]
        else:
            raise ValueError("Invalid register index")

    def control_unit(self, instruction, reg_a_index, reg_b_index, dest_reg_index=None):
        """
        The Control Unit (CU) orchestrates the operation.
        It fetches values from registers, checks cache, directs ALU, and stores results.
        """
        # 1. Fetch values from registers (The "Hands")
        val_a = self.registers[reg_a_index]
        val_b = self.registers[reg_b_index]

        # 2. Check Cache (The "Countertop")
        cache_key = (instruction, val_a, val_b)
        if cache_key in self.cache:
            print(f"Cache Hit! Retrieved result for {instruction} {val_a}, {val_b}")
            result = self.cache[cache_key]
        else:
            # 3. If not in cache, send to ALU (The "Worker")
            print(f"Cache Miss. Sending to ALU for {instruction} {val_a}, {val_b}")
            result = self._alu_dispatch(instruction, val_a, val_b)
            
            # 4. Store result in Cache
            self.cache[cache_key] = result

        # 5. Store result back in a register if a destination is provided
        # If no destination is provided, we default to storing in reg_a_index (common in some architectures)
        target_reg = dest_reg_index if dest_reg_index is not None else reg_a_index
        self.registers[target_reg] = result
        return result

    def _alu_dispatch(self, instruction, a, b):
        """Internal method acting as the ALU."""
        if instruction == "ADD":
            return self.add(a, b)
        elif instruction == "SUB":
            return self.sub(a, b)
        elif instruction == "MUL":
            return self.mul(a, b)
        elif instruction == "DIV":
            return self.div(a, b)
        elif instruction == "MOD":
            return self.mod(a, b)
        elif instruction == "POW":
            return self.pow(a, b)
        elif instruction == "AND":
            return self.logi_and(a, b)
        elif instruction == "OR":
            return self.logi_or(a, b)
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    # --- ALU Operations ---
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ValueError("Can't divide by zero")
        return a / b

    def mod(self, a, b):
        if b == 0:
            raise ValueError("Can't divide by zero")
        return a % b

    def pow(self, a, b):
        return a ** b

    def sqrt(self, a):
        return a ** 0.5

    def log(self, a, b):
        return math.log(a, b)

    def logi_and(self, a, b):
        return a & b

    def logi_or(self, a, b):
        return a | b

if __name__ == "__main__":
    cpu = CPU()
    
    print("--- Initial State ---")
    print(f"Registers: {cpu.registers}")
    print(f"Cache: {cpu.cache}")

    print("\n--- Loading Values ---")
    cpu.load(0, 10) # R0 = 10
    cpu.load(1, 5)  # R1 = 5
    print(f"Registers: {cpu.registers}")

    print("\n--- Executing ADD (R0 + R1 -> R2) ---")
    # Instruction: ADD, Reg A: 0, Reg B: 1, Store in Reg: 2
    result = cpu.control_unit("ADD", 0, 1, 2)
    print(f"Result: {result}")
    print(f"Registers: {cpu.registers}")
    print(f"Cache: {cpu.cache}")

    print("\n--- Executing ADD Again (Cache Hit Check) ---")
    # Should hit cache
    result = cpu.control_unit("ADD", 0, 1, 2)
    print(f"Result: {result}")

    print("\n--- Executing MUL (R0 * R1 -> R3) ---")
    cpu.control_unit("MUL", 0, 1, 3)
    print(f"Registers: {cpu.registers}")
    
    print("\n--- Complex Operation: (R2 + R3) -> R0 ---")
    # R2 is 15 (from ADD), R3 is 50 (from MUL)
    cpu.control_unit("ADD", 2, 3, 0)
    print(f"Registers: {cpu.registers}")