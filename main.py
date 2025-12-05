import simple_os.simulation_utils as utils
from simple_os.process.process_manager import ProcessManager
from simple_os.process.scheduler import Scheduler

import argparse

def simulate_os(
    to_be_created_procs_list: utils.ProcCreatedTimedList,
    filesystem_state,  # FileSystemManager
    filesystem_operations: list,  # List of file operations
):
    # time for debugging purposes
    max_os_execution_time = 1e8
    t = 0
    processes_left_to_run = to_be_created_procs_list.num_procs

    while (
        t < max_os_execution_time and
        processes_left_to_run > 0
    ):
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

        exec_time, proc = Scheduler.get_next_exec_time_and_proc()
        interrupted_at = 0
        interrupted = False
        if proc is None:
            t += 1
            continue

        while not interrupted and interrupted_at < exec_time:
            interrupted_at += 1
            just_arrived_procs_to_create = to_be_created_procs_list.get_unfetched_procs_until(
                t + interrupted_at
            )

            for just_arrived_proc in just_arrived_procs_to_create:
                ProcessManager.create_process(
                    just_arrived_proc.priority,
                    just_arrived_proc.execution_time,
                    just_arrived_proc.memory_needed,
                    just_arrived_proc.requested_printer,
                    just_arrived_proc.requested_scanner,
                    just_arrived_proc.requested_modem,
                    just_arrived_proc.requested_disk,
                )
                if just_arrived_proc.priority < proc.priority:
                    # current process just got interrupted
                    interrupted = True
                    break

        t += interrupted_at

        Scheduler.dispatch(proc, exec_time, interrupted_at)

        if proc.time_left == 0:
            # NOTE: terminate should also
            # check for blocked process that may be unblocked
            processes_left_to_run -= 1
            ProcessManager.terminate_process(proc.pid)

    # After process simulation finishes, execute file system operations (if any)
    try:
        if filesystem_operations:
            print("Sistema de arquivos =>")
            for i in range(len(to_be_created_procs_list._procs_to_be_created)):
                if to_be_created_procs_list._procs_to_be_created[i].priority == 0:
                    filesystem_state.add_real_time_process(i)
                else:
                    filesystem_state.add_process(i)

            filesystem_state.execute_all_operations()
            filesystem_state.show_current_state()

    except Exception as e:
        print("File system integration error:", e)


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

    to_be_created_list = utils.parse_procs_decl(args.procs)

    ops, fs_manager = utils.parse_file_decl(args.files)

    simulate_os(
        to_be_created_list,
        fs_manager,
        ops,
    )


if __name__ == "__main__":
    main()
