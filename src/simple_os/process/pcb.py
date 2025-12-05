import typing
from dataclasses import dataclass
from enum import Enum, auto

class ProcState(Enum):
    READY = auto()
    BLOCKED = auto()
    RUNNING = auto()
    EXIT = auto()


class ProcBlockedReason(Enum):
    WAITING_FOR_MEM = auto()
    TOO_LARGE_MEM_REQUEST = auto()
    WAITING_FOR_IO = auto()
    # ...

@dataclass
class PCB:
    # generic properties
    pid: int
    starting_priority: int
    time_needed: int
    is_preemptable: bool
    marked_for_termination: bool
    # memory props
    memory_needed: int
    memory_offset: typing.Optional[int]
    memory_num_allocated_blocks: typing.Optional[int]
    # scheduler and running props
    time_left: int
    priority: int
    state: ProcState
    blocked_reason: typing.Optional[ProcBlockedReason]
    pc: int
    # i/o status
    using_scanner: bool
    requested_printer: int
    using_modem: bool
    requested_sata: int

    @property
    def using_io(self):
        return (
            self.using_scanner
            or self.using_modem
            or self.requested_printer
            or self.requested_sata
        )

