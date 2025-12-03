from simple_os.process.pcb import PCB, ProcState
import simple_os.simulation_utils as utils
from simple_os.process.process_manager import ProcessManager
from simple_os.process.scheduler import Scheduler

import argparse
import sys

from pathlib import Path

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
    dispatcher_timed_list: utils.DispatcherTimedList,
    filesystem_state: utils.FileSystemState,
    filesystem_operations: utils.FileSystemOperations,
):
    # time for debugging purposes
    max_os_execution_time = sys.maxsize
    t = 0
    processes_left_to_run = dispatcher_timed_list.num_procs

    while (
        # for DEBUGGING
        t < max_os_execution_time and
        processes_left_to_run > 0
    ):
        # TODO: dispatch processes up to the current time
        just_arrived_procs_to_dispatch = dispatcher_timed_list.get_unfetched_procs_until(t)

        for proc in just_arrived_procs_to_dispatch:
            ProcessManager.create_process()

        # TODO: run scheduler to get next proc
        proc_and_exec_time = Scheduler.get_next_proc()
        if proc_and_exec_time is None:
            t += 1
            continue
        exec_time, proc = proc_and_exec_time

        print("proc.time_needed", proc.time_needed)
        while exec_time > 0:
            print(f"EXECUTING {proc.pid}, PC={proc.pc}, time_left={proc.time_left}")
            exec_time -= 1
            proc.pc += 1
            proc.time_left -= 1
        # exit()
        if proc.time_left == 0:
            # NOTE: terminate should also
            # check for blocked process that may be unblocked
            processes_left_to_run -= 1
            ProcessManager.terminate_process(proc.pid)

        t += exec_time


def main():
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

    dispatch_timed_list = utils.parse_procs_decl(args.procs)
    print("dispatch_timed_list._procs_to_be_dispatched", dispatch_timed_list._procs_to_be_dispatched)

    ops, initial_state = utils.parse_file_decl(args.files)

    simulate_os(
        dispatch_timed_list,
        ops,
        initial_state,
    )

    print("Hello from simple-os-sim!")


if __name__ == "__main__":
    main()
