from simple_os.process.pcb import PCB, ProcState, ProcBlockedReason

class ProcessManager:
    MAX_PROCS = 100

    def __init__(self, memory_manager, scheduler):
        self.process_manager: list[typing.Optional[PCB]] = [None] * self.MAX_PROCS
        self.next_pid = 0
        self.scheduler = scheduler
        self.memory_manager = memory_manager

    def _add_pcb_to_table(self, pcb: PCB):
        i = 0
        # find first allocation space for process
        while self.procs[i] is not None:
            i += 1

        self.procs[i] = pcb

    def create_process(self) -> PCB:
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
            self.scheduler.dispatch()

        self.next_pid += 1

    def terminate_process(pid: int):
        self.memo
