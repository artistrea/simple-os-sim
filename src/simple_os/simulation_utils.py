from dataclasses import dataclass, field

@dataclass
class ProcToBeDispathed:
    created_at: int  # time start
    priority: int
    execution_time: int
    memory_needed: int
    requested_printer: int
    requested_scanner: int
    requested_modem: int
    requested_disk: int
    

@dataclass
class ProcCreatedTimedList:
    # sorted by created_at list of processes to be created
    _procs_to_be_created: list[ProcToBeDispathed] = field(default_factory=list)
    created_until_idx: int = 0

    def append(self, item: ProcToBeDispathed):
        # stable sorted insert into procs to be created
        # maintains order of processes at the same time
        # NOTE: O(N) insert is quite alright considering the simulation scope
        i = 0
        while (
            i < self.num_procs and
            item.created_at <= self._procs_to_be_created[i].created_at
        ):
            i += 1
        self._procs_to_be_created.insert(i, item)

    @property
    def num_procs(self):
        return len(self._procs_to_be_created)

    def get_unfetched_procs_until(self, t: int):
        start = self.created_until_idx
        while (
            self.created_until_idx < self.num_procs and
            self._procs_to_be_created[self.created_until_idx].created_at <= t
        ):
            self.created_until_idx += 1
        return self._procs_to_be_created[start:self.created_until_idx]

@dataclass
class FileSystemState:
    pass

@dataclass
class FileSystemOperations:
    pass

def parse_procs_decl(path: str):
    to_be_created_list = ProcCreatedTimedList()
    with open(path, "r") as f:
        for line in f:
            if len(line) == 0:
                continue
            try:
                to_be_created_list.append(
                    ProcToBeDispathed(
                        *list(map(lambda x: int(x.strip()), line.split(",")))
                    )
                )
            except Exception as e:
                print(f"Could not parse processes file {path}")
                raise e

    return to_be_created_list

def parse_file_decl(path: str):
    return FileSystemOperations(), FileSystemState()


