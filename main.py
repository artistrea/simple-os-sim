from simple_os.process.pcb import PCB, ProcState
import simple_os.simulation_utils as utils
from simple_os.process.process_manager import ProcessManager
from simple_os.process.scheduler import Scheduler

import argparse
import sys

def simulate_os(
    to_be_created_procs_list: utils.ProcCreatedTimedList,
    filesystem_state: utils.FileSystemState,
    filesystem_operations: utils.FileSystemOperations,
):
    # time for debugging purposes
    max_os_execution_time = sys.maxsize
    t = 0
    processes_left_to_run = to_be_created_procs_list.num_procs

    while (
        # for DEBUGGING
        t < max_os_execution_time and
        processes_left_to_run > 0
    ):
        # TODO: create processes up to the current time
        just_arrived_procs_to_create = to_be_created_procs_list.get_unfetched_procs_until(t)

        for proc in just_arrived_procs_to_create:
            ProcessManager.create_process(
                proc.priority,
                proc.execution_time,
                proc.memory_needed,
                proc.requested_printer,
                proc.requested_scanner,
                proc.requested_modem,
                proc.requested_disk,
            )

        # TODO: run scheduler to get next proc
        proc_and_exec_time = Scheduler.get_next_exec_time_and_proc()
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

    to_be_created_list = utils.parse_procs_decl(args.procs)
    print("to_be_created_list._procs_to_be_created", to_be_created_list._procs_to_be_created)

    ops, initial_state = utils.parse_file_decl(args.files)

    simulate_os(
        to_be_created_list,
        ops,
        initial_state,
    )

    print("Hello from simple-os-sim!")


if __name__ == "__main__":
    main()
