from simple_os.process.pcb import PCB, ProcState
from simple_os.cpu import CPU
import typing

# definition of what would be in a c module about the scheduler
class _Scheduler:
    NUM_QUEUES = 6
    MAX_PROCS = 100

    QUANTUM_TABLE = {
        0: None,  # real time, no preempting
        1: 6,
        2: 5,
        3: 4,
        4: 3,
        5: 2,
    }

    def __init__(self):
        # the queues keep indices for process table lookup
        self.queues: list[list[int]] = [[] for _ in range(self.NUM_QUEUES)]
        # uninitialized process table
        self.process_table: list[typing.Optional[PCB]] = None
        
        # for aging
        self.waiting_time = {}  # indice -> waiting time

    def apply_aging(self, t: int):
        """Makes processes higher priority depending on waiting time.
        This prevents starvation.
        """
        for prio in range(2, 6):
            updated_queue = []
            for pid in self.queues[prio]:
                self.waiting_time[pid] += t

                if self.waiting_time[pid] >= 20 and prio > 1:
                    pcb = self.process_table[pid]
                    pcb.priority -= 1
                    self.queues[prio - 1].append(pid)
                    self.waiting_time[pid] = 0
                else:
                    updated_queue.append(pid)

            self.queues[prio] = updated_queue

    def register_process_table(self, process_table: list[typing.Optional[PCB]]):
        self.process_table = process_table

    def add_ready_process(
        self,
        pcb: PCB,
    ) -> int:
        assert pcb.state == ProcState.READY

        assert 0 <= pcb.priority <= 5
        self.queues[pcb.priority].append(pcb.pid)
        self.waiting_time[pcb.pid] = 0

    def get_next_exec_time_and_proc(self) -> (int, PCB):
        if self.queues[0]:
            pid = self.queues[0].pop(0)
            pcb = self.process_table[pid]

            assert pcb.state == ProcState.READY

            return pcb.time_left, pcb  # sem preempção

        for prio in range(1, 6):
            if self.queues[prio]:
                pid = self.queues[prio].pop(0)
                pcb = self.process_table[pid]

                assert pcb.state == ProcState.READY

                quantum = self.QUANTUM_TABLE[prio]
                self.waiting_time[pid] = 0

                return min(quantum, pcb.time_left), pcb

        return None, None

    def requeue_after_execution(self, pcb: PCB):
        """
        Chamado pelo process manager depois que o PCB executou por um quantum.
        Só realimenta se ainda não terminou.
        """
        if pcb.time_left <= 0:
            return

        if pcb.priority < 5:
            pcb.priority += 1

        self.add_ready_process(pcb)

    def dispatch(self, proc: PCB, exec_time: int, interrupted_at: int):
        proc.state = ProcState.RUNNING
        print()
        print(f"""dispatcher =>
    PID: {proc.pid}
    offset: {proc.memory_offset}
    blocks: {proc.memory_num_allocated_blocks}
    priority: {proc.priority}
    starting_priority: {proc.starting_priority}
    allocated_time: {exec_time}
    time_left: {proc.time_left}
    scanners: {1 if proc.using_scanner else 0}
    printers: {proc.requested_printer}
    modems: {1 if proc.using_modem else 0}
    sata: {proc.requested_sata}"""
        )
        CPU.execute(proc, exec_time, interrupted_at)
        proc.state = ProcState.READY
        self.apply_aging(interrupted_at)
        self.requeue_after_execution(proc)


Scheduler = _Scheduler()
