from simple_os.process.pcb import PCB

class _CPU:
    def execute(self, proc: PCB, exec_time: int):
        assert exec_time <= proc.time_left
        print()
        print(f"process {proc.pid} =>")
        if proc.time_left == proc.time_needed:
            print(f"P{proc.pid} STARTED")
        while exec_time > 0:
            print(f"P{proc.pid} instruction {proc.pc + 1}")
            exec_time -= 1
            proc.pc += 1
            proc.time_left -= 1

        if proc.time_left == 0:
            print(f"P{proc.pid} return SIGINT")

CPU = _CPU()
