import typing
from dataclasses import dataclass
from enum import Enum, auto

class ProcState(Enum):
    READY = auto()
    BLOCKED = auto()
    RUNNING = auto()


class ProcBlockedReason(Enum):
    WAITING_FOR_MEM = auto()
    WAITING_FOR_IO = auto()
    # ...

@dataclass
class PCB:
    # generic properties
    pid: int
    starting_priority: int
    time_needed: int
    is_preemptable: bool
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

