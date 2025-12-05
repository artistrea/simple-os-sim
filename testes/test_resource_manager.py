from ResourceManager import _ResourceManager

# Helpers

def alloc_ok(rm, *args, **kwargs):
    ok, _ = rm.request_resources(*args, **kwargs)
    return ok

def alloc_fail(rm, *args, **kwargs):
    ok, _ = rm.request_resources(*args, **kwargs)
    return not ok

# 1. Testes simples

def test_scanner_basic():
    rm = _ResourceManager()

    assert alloc_ok(rm, 1, need_scanner=True)
    assert alloc_fail(rm, 2, need_scanner=True)  # ocupado
    rm.release_resources(1)
    assert alloc_ok(rm, 2, need_scanner=True)


def test_modem_basic():
    rm = _ResourceManager()

    assert alloc_ok(rm, 1, need_modem=True)
    assert alloc_fail(rm, 2, need_modem=True)
    rm.release_resources(1)
    assert alloc_ok(rm, 2, need_modem=True)


def test_specific_printer():
    rm = _ResourceManager()

    assert alloc_ok(rm, 1, printer_idx=0)
    assert alloc_fail(rm, 2, printer_idx=0)


def test_any_printer():
    rm = _ResourceManager()

    ok, msg = rm.request_resources(1, printer_idx=-1)
    assert ok
    assert "printer[0]" in msg

    ok, msg = rm.request_resources(2, printer_idx=-1)
    assert ok
    assert "printer[1]" in msg

    assert alloc_fail(rm, 3, printer_idx=-1)  # nenhuma livre

# 2. Disputa de I/O

def test_two_process_scanner_competition():
    rm = _ResourceManager()

    assert alloc_ok(rm, 1, need_scanner=True)
    assert alloc_fail(rm, 2, need_scanner=True)
    rm.release_resources(1)
    assert alloc_ok(rm, 2, need_scanner=True)


def test_multiple_resources_needed():
    rm = _ResourceManager()

    rm.request_resources(1, need_scanner=True)
    rm.request_resources(2, need_modem=True)

    assert alloc_fail(rm, 3, need_scanner=True, need_modem=True)

    rm.release_resources(1)
    assert alloc_fail(rm, 3, need_scanner=True, need_modem=True)

    rm.release_resources(2)
    assert alloc_ok(rm, 3, need_scanner=True, need_modem=True)

# 3. Reentrância (pede em etapas)

def test_reentrant_allocation():
    rm = _ResourceManager()

    assert alloc_ok(rm, 4, need_scanner=True)
    assert alloc_ok(rm, 4, need_modem=True)
    assert alloc_ok(rm, 4, printer_idx=1)

    assert rm.scanner == 4
    assert rm.modem == 4
    assert rm.printers[1] == 4


# 4. Liberar recursos

def test_release_single_resource():
    rm = _ResourceManager()

    rm.request_resources(8, printer_idx=1, need_modem=True)
    rm.release_printer(8, 1)

    assert rm.printers[1] is None
    assert rm.modem == 8


def test_release_all():
    rm = _ResourceManager()

    rm.request_resources(9, need_scanner=True, printer_idx=0, need_modem=True, sata_idx=2)
    rm.release_resources(9)

    assert rm.scanner is None
    assert rm.modem is None
    assert rm.printers == [None, None]
    assert rm.sata == [None, None, None]

# 5. SATA tests

def test_specific_sata():
    rm = _ResourceManager()

    assert alloc_ok(rm, 10, sata_idx=2)
    assert alloc_fail(rm, 11, sata_idx=2)


def test_any_sata():
    rm = _ResourceManager()

    ok, msg = rm.request_resources(10, sata_idx=-1)
    assert ok
    assert "sata[0]" in msg

    ok, msg = rm.request_resources(11, sata_idx=-1)
    assert ok
    assert "sata[1]" in msg

    ok, msg = rm.request_resources(12, sata_idx=-1)
    assert ok
    assert "sata[2]" in msg

    assert alloc_fail(rm, 13, sata_idx=-1)

# 6. Bloqueio por recurso (simulado sem scheduler)

def test_blocked_then_unblocked_resource():
    rm = _ResourceManager()

    rm.request_resources(20, printer_idx=0)
    assert alloc_fail(rm, 21, printer_idx=0)

    rm.release_resources(20)
    assert alloc_ok(rm, 21, printer_idx=0)

# 7. Casos complexos

def test_process_needing_two_resources_waits_for_both():
    rm = _ResourceManager()

    rm.request_resources(1, need_scanner=True)
    rm.request_resources(2, printer_idx=0)

    assert alloc_fail(rm, 3, need_scanner=True, printer_idx=0)

    rm.release_resources(1)
    assert alloc_fail(rm, 3, need_scanner=True, printer_idx=0)

    rm.release_resources(2)
    assert alloc_ok(rm, 3, need_scanner=True, printer_idx=0)

# 8. Testes de erro

def test_invalid_printer_index():
    rm = _ResourceManager()
    assert alloc_fail(rm, 1, printer_idx=99)


def test_invalid_sata_index():
    rm = _ResourceManager()
    assert alloc_fail(rm, 1, sata_idx=-2)

def test_reentrant_idempotent():
    rm = _ResourceManager()

    assert alloc_ok(rm, 5, printer_idx=1)
    assert alloc_ok(rm, 5, printer_idx=1)
    assert rm.printers[1] == 5

def test_reentrant_sata():
    rm = _ResourceManager()

    assert alloc_ok(rm, 7, sata_idx=2)
    assert alloc_ok(rm, 7, sata_idx=2)
    assert rm.sata[2] == 7
