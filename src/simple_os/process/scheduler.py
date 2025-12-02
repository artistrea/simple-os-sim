from simple_os.process.pcb import PCB
from dataclasses import dataclass
import typing

# definition of what would be in a c module about the scheduler
class _Scheduler:
    NUM_QUEUES = 6
    MAX_PROCS = 100

    QUANTUM_TABLE = {
        0: None,  # tempo real, sem preempção
        1: 6,
        2: 5,
        3: 4,
        4: 3,
        5: 2,
    }

    def __init__(self, process_manager: "ProcessManager"):
        self.process_manager: list[typing.Optional[PCB]] = [None] * self.MAX_PROCS
        self.queues: list[list[int]] = [[] for _ in range(self.NUM_QUEUES)]

    def add_proc(
        self,
        pcb: PCB
    ) -> int:
        i = 0
        # find first allocation space for process
        while self.procs[i] is not None:
            i += 1

        self.procs[i] = pcb

    def get_next_proc(self):
