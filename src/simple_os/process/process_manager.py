from simple_os.process.pcb import PCB, ProcState, ProcBlockedReason
from simple_os.process.scheduler import Scheduler
from simple_os.memory.MemoryManager import MemoryManager
import typing

class _ProcessManager:
    MAX_PROCS = 100

    def __init__(self, memory_manager, scheduler):
        self.process_table: list[typing.Optional[PCB]] = [None] * self.MAX_PROCS
        self.next_pid = 0
        self.scheduler = scheduler
        scheduler.register_process_table(self.process_table)
        self.memory_manager = memory_manager

    def _add_pcb_to_table(self, pcb: PCB):
        i = 0
        # find first allocation space for process
        while self.process_table[i] is not None:
            i += 1

        self.process_table[i] = pcb

    def _free_pid_from_table(self, pid: int):
        i = 0
        # find first allocation space for process
        while i < self.MAX_PROCS and (
            self.process_table[i] is None or self.process_table[i].pid != pid
        ):
            i += 1
        if i == self.MAX_PROCS:
            raise ValueError("AOPA")

        self.process_table[i] = None

    def create_process(self):
        # TODO: add args
        # TODO: allocate memory
        # TODO: allocate resources
        pcb = PCB(
            pid=self.next_pid,
            starting_priority=0,
            time_needed=10,
            is_preemptable=False,
            # memory props
            memory_needed=16,
            memory_offset = None,
            memory_num_allocated_blocks = None,
            # scheduler and running props
            time_left=10,
            priority=0,
            state=ProcState.READY,
            blocked_reason=None,
            pc=0,
            # i/o status
            using_scanner=False,
            using_printer=False,
            using_modem=False,
            using_sata=False,
        )
        mem_offset = self.memory_manager.allocate(
            pcb.memory_needed, pcb.priority
        )
        if mem_offset == -1:
            pcb.state = ProcState.BLOCKED
            pcb.blocked_reason = ProcBlockedReason.WAITING_FOR_MEM
        # IO allocator

        self._add_pcb_to_table(pcb)
        if pcb.state == ProcState.READY:
            self.scheduler.dispatch(pcb)

        self.next_pid += 1

    def terminate_process(self, pid: int):
        self._free_pid_from_table(pid)
        # TODO: memory management blocked processes list
        pass
        # self.memo

ProcessManager = _ProcessManager(MemoryManager, Scheduler)
