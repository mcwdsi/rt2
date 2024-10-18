from rt_core_v2.ids_codes.rui import Rui, TempRef, ID_Rui
from uuid6 import uuid7
from datetime import datetime, timezone


def print_info(rui):
    print(rui)
    print("\tassigned? " + str(rui.is_assigned()))
    print("\treserved? " + str(rui.is_reserved()))
    print("\tuuid: " + str(rui.uuid))


def print_tr(tr):
    print(tr)
    print("ref field=", tr.ref)


def test_ruistatus():
    default_rui_1 = ID_Rui()
    default_rui_2 = ID_Rui()

    uuid_1 = uuid7()
    uuid_2 = uuid7()
    set_rui_1 = ID_Rui(uuid_1)
    set_rui_2 = ID_Rui(uuid_2)
    clone_rui_1 = ID_Rui(uuid_1)

    assert default_rui_1.uuid != default_rui_2.uuid
    assert set_rui_1.uuid != set_rui_2.uuid
    assert set_rui_1.uuid == clone_rui_1.uuid


def test_tempref():
    j = TempRef(uuid7())
    k = TempRef(datetime.now(timezone.utc))
    m = TempRef(datetime.now())
    n = TempRef(None)
    p = TempRef(None)

    assert j.ref != n.ref and k.ref != m.ref

    print("\n### Temporal reference initialized with UUID ###")
    print_tr(j)
    print("##############\n")

    print("### Temporal reference initialized with UTC now ###")
    print_tr(k)
    print("##############\n")

    print("### Temporal reference initialized with local now ###")
    print_tr(m)
    print("##############\n")

    print(
        "### Temporal reference initialized with no id and instruction to create a new UUID ###"
    )
    print_tr(n)
    print("##############\n")

    print(
        "### Temporal reference initialized with no id and instruction to create a UTC now datetime ###"
    )
    print_tr(p)
    print("##############\n")
