from simple_os.process.pcb import PCB, ProcState

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DispatcherTimedList:
    pass

@dataclass
class FileSystemState:
    pass

@dataclass
class FileSystemOperations:
    pass

def parse_procs_decl(path: str):
    return DispatcherTimedList()

def parse_file_decl(path: str):
    return FileSystemOperations(), FileSystemState()

def get_next_proc():
    return PCB(
        pid=0,
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

def simulate_os(
    dispatcher_timed_list: DispatcherTimedList,
    filesystem_state: FileSystemState,
    filesystem_operations: FileSystemOperations,
    max_os_execution_time: int = None,
):
    if max_os_execution_time == None:
        max_os_execution_time = sys.maxsize
        print("max_os_execution_time", max_os_execution_time)

    t = 0

    while t < max_os_execution_time:
        # TODO: dispatch processes up to the current time
        # TODO: run scheduler to get next proc
        proc = get_next_proc()
        # if 
        t += 1


def main():
    # for debugging purposes:
    MAX_OS_EXEC_TIME = 10
    parser = argparse.ArgumentParser(description="TODO")
    

    parser.add_argument(
        "--procs", "-p",
        type=str,
        help="TODO",
    )

    parser.add_argument(
        "--files", "-f",
        type=str,
        help="TODO"
    )
    args = parser.parse_args()

    print("args.files", args.files)
    print("args.procs", args.procs)

    ops, initial_state = parse_file_decl(args.files)
    dispatch_timed_list = parse_procs_decl(args.files)

    simulate_os(
        dispatch_timed_list,
        ops,
        initial_state,
        MAX_OS_EXEC_TIME
    )

    print("Hello from simple-os-sim!")


if __name__ == "__main__":
    main()
