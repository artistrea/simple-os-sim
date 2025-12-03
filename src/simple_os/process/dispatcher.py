from simple_os.cpu import CPU
from simple_os.process.pcb import PCB

class _Dispatcher:
    def dispatch(self, proc: PCB, exec_time: int):
        print()
        print(f"""dispatcher =>
    PID: {proc.pid}
    offset: {proc.memory_offset}
    blocks: {proc.memory_num_allocated_blocks}
    priority: {proc.priority}
    allocated_time: {exec_time}
    time_left: {exec_time}
    scanners: {0 if proc.using_scanner else 1}
    printers: {proc.requested_printer}
    modems: {0 if proc.using_modem else 1}
    sata: {proc.requested_sata}"""
        )
        CPU.execute(proc, exec_time)

Dispatcher = _Dispatcher()
