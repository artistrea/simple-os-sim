from simple_os.memory.Memory import Memory

class MemoryManager:
    def __init__(self):
        self.memory = Memory() # instancia Memory

    def find_contiguous_space(self, start, end, size): # busca por segmento contíguo de memória
        free_count = 0
        initial_index = -1

        for i in range(start, end):
            if self.memory.blocks[i] is None:
                if free_count == 0:
                    initial_index = i

                free_count = free_count + 1 # atualiza espaço encontrado

                if free_count == size:
                    return initial_index
            else:
                free_count = 0 # espaço alocado

        return -1

    def allocate(self, pid, size, is_real_time = False): # aloca memória ao processo
        if is_real_time:
            start = 0
            end = 64
        else:
            start = 64
            end = 1024

        offset = self.find_contiguous_space(start, end, size)

        if offset == -1:
            return None

        for i in range(offset, offset + size):
            self.memory.blocks[i] = pid # associa bloco de memória a um PID

        return offset

    def free(self, pid): # libera memória do processo
        for i in range(self.memory.total_blocks):
            if self.memory.blocks[i] == pid:
                self.memory.blocks[i] = None
