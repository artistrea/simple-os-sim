from simple_os.process.pcb import PCB, ProcState, ProcBlockedReason
from simple_os.process.scheduler import Scheduler
from simple_os.memory.MemoryManager import MemoryManager
import typing

class _ProcessManager:
    MAX_PROCS = 100

    def __init__(self, memory_manager, scheduler):
        self.process_table: list[typing.Optional[PCB]] = [None] * self.MAX_PROCS
        self.blocked_procs = []
        self.next_pid = 0
        self.scheduler = scheduler
        scheduler.register_process_table(self.process_table)
        self.memory_manager = memory_manager

    def _get_proc_table_idx(self, pid: int) -> int:
        i = 0
        # find first allocation space for process
        while i < self.MAX_PROCS and (
            self.process_table[i] is None or self.process_table[i].pid != pid
        ):
            i += 1

        # TODO: remove this assertion
        assert i != self.MAX_PROCS

        return i

        
    def _add_pcb_to_table(self, pcb: PCB) -> int:
        i = 0
        # find first allocation space for process
        while self.process_table[i] is not None:
            i += 1

        self.process_table[i] = pcb

        return i

    def _free_pid_from_table(self, pid: int):
        i = self._get_proc_table_idx(pid)

        # TODO: add error instead of assertion
        assert i != self.MAX_PROCS

        self.process_table[i] = None

    def create_process(
        self,
        priority: int,
        execution_time: int,
        memory_needed: int,
        requested_printer: int,
        requested_scanner: int,
        requested_modem: int,
        requested_disk: int,
    ):
        # TODO: allocate resources
        pcb = PCB(
            pid=self.next_pid,
            starting_priority=priority,
            time_needed=execution_time,
            is_preemptable=priority == 0,
            # memory props
            memory_needed=memory_needed,
            memory_offset=None,
            memory_num_allocated_blocks=memory_needed,
            # scheduler and running props
            time_left=execution_time,
            priority=0,
            state=ProcState.READY,
            blocked_reason=None,
            pc=0,
            # i/o status
            using_scanner=requested_scanner == 1,
            requested_printer=requested_printer,
            using_modem=requested_modem == 1,
            requested_sata=requested_disk,
        )
        mem_offset = self.memory_manager.allocate(
            pcb.pid, pcb.memory_needed, pcb.priority == 0
        )
        if mem_offset is None:
            pcb.state = ProcState.BLOCKED
            pcb.blocked_reason = ProcBlockedReason.WAITING_FOR_MEM
        # IO allocator

        self._add_pcb_to_table(pcb)

        if pcb.state == ProcState.READY:
            self.scheduler.dispatch(pcb)
        else:
            self.blocked_procs.append(pcb.pid)

        self.next_pid += 1

    def terminate_process(self, pid: int):
        self._free_pid_from_table(pid)
        self.memory_manager.free(pid)
        # TODO: memory management blocked processes list
        pass
        # self.memo

ProcessManager = _ProcessManager(MemoryManager, Scheduler)
