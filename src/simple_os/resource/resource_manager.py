class _ResourceManager:
    def __init__(self): # inicializa 1 scanner, 2 impressoras, 1 modem e 3 SATA
        self.scanner = None # cada recurso associado a None ou a um PID
        self.printers = [None, None]
        self.modem = None
        self.sata = [None, None, None]

    def _is_printer_free(self, idx):
        if ((0 <= idx < len(self.printers)) and (self.printers[idx] is None)):
            return True
        else:
            return False

    def _is_sata_free(self, idx):
        if ((0 <= idx < len(self.sata)) and (self.sata[idx] is None)):
            return True
        else:
            return False

    def request_resources(self, pid, need_printer = False, need_scanner = False, need_modem = False, need_sata = False): # aloca recurso
        if need_scanner and self.scanner is not None and self.scanner is not pid: # checa impressora
            return False, f"Scanner busy (held by PID {self.scanner})"

        if need_modem and self.modem is not None and self.modem is not pid: # checa modem
            return False, f"Modem busy (held by PID {self.modem})"

        printer_idx = None
        if need_printer: # qualquer impressora disponível
            avail = None
            i = 0
            already_has = False
            for p in self.printers: # busca primeira impressora disponível
                if p is None:
                    avail = i
                if p == pid:
                    already_has = True
                i = i + 1
            if already_has:
                pass
            elif avail is None:
                return False, "todas impressoras ocupadas"
            printer_idx = avail

        sata_idx = None
        if need_sata: # qualquer SATA disponível
            avail = None
            already_has = False
            i = 0
            for p in self.sata: # busca primeiro SATA disponível
                if p is None:
                    avail = i
                if p == pid:
                    already_has = True
                i = i + 1 # define índice de SATA
            if already_has:
                pass
            elif avail is None:
                return False, "todos dispositivos SATA ocupados"

            sata_idx = avail

        if need_scanner:
            self.scanner = pid

        if need_modem:
            self.modem = pid

        if printer_idx is not None:
            self.printers[printer_idx] = pid

        if sata_idx is not None:
            self.sata[sata_idx] = pid

        allocated_parts = []
        if need_scanner:
            allocated_parts.append("scanner")

        if need_modem:
            allocated_parts.append("modem")

        if printer_idx is not None:
            allocated_parts.append(f"printer[{printer_idx}]")

        if sata_idx is not None:
            allocated_parts.append(f"sata[{sata_idx}]")

        msg = f"Recursos alocados ao PID {pid}: {', '.join(allocated_parts) if allocated_parts else 'none'}"
        return True, msg

    def release_resources(self, pid): # libera recurso
        released = []
        if self.scanner == pid:
            self.scanner = None
            released.append("scanner")

        i = 0
        for p in self.printers: # libera impressora associada ao PID
            if p == pid:
                self.printers[i] = None
                released.append(f"printer[{i}]")
                break
            i = i + 1

        if self.modem == pid:
            self.modem = None
            released.append("modem")

        i = 0
        for d in self.sata: # libera SATA associada ao PID
            if d == pid:
                self.sata[i] = None
                released.append(f"sata[{i}]")
                break
            i = i + 1

        if released:
            return True, f"Recursos liberados associados ao PID {pid}: {', '.join(released)}"
        else:
            return False, f"Nenhum recurso associado ao PID {pid}"

    def release_printer(self, pid, idx): # libera impressora
        if 0 <= idx < len(self.printers) and self.printers[idx] == pid:
            self.printers[idx] = None
            return True
        return False

    def release_sata(self, pid, idx): # libera sata
        if 0 <= idx < len(self.sata) and self.sata[idx] == pid:
            self.sata[idx] = None
            return True
        return False

    def __str__(self):
        return f"Scanner: {self.scanner}, Printers: {self.printers}, Modem: {self.modem}, SATA: {self.sata}"

ResourceManager = _ResourceManager()
