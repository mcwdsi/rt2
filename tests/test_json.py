import json

from rt_core_v2.rttuple import *
from rt_core_v2.rttuple_formatter import format_rttuples

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    

def test_json():
    ruip = Rui()
    ruia = Rui()
    ruit= Rui()

    atuple_1 = Atuple(ruip, ruia, ruit)
    formated_1 = format_rttuples(atuple_1)
    print(formated_1)
    expected_1 = f"{{\"ruip\": \"{ruip}\", \"ruia\": \"{ruia}\", \"ruit\": \"{ruit}\", \"type\": \"{atuple_1.tuple_type}\", \"unique\": \"{atuple_1.unique}\", \"ar\": \"{atuple_1.ar}\", \"t\": \"{atuple_1.t}\"}}"
    print(expected_1)
    assert(ordered(json.loads(formated_1)) == ordered(json.loads(expected_1)))
