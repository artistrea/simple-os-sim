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

    def __init__(self):
        self.queues: list[list[int]] = [[] for _ in range(self.NUM_QUEUES)]
        # uninitialized process table
        self.process_table: list[typing.Optional[PCB]] = None

    def register_process_table(self, process_table: list[typing.Optional[PCB]]):
        self.process_table = process_table

    def add_ready_process(
        self,
        pcb: PCB,
    ) -> int:
        pass

    def get_next_exec_time_and_proc(self) -> (int, PCB):
        i = 0

        while i < self.MAX_PROCS and self.process_table[i] is None:
            i += 1

        if i == self.MAX_PROCS:
            return None

        return self.process_table[i].time_needed, self.process_table[i]

Scheduler = _Scheduler()
