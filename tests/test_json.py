import json

from rt_core_v2.ids_codes.Rui import Rui, TempRef
from rt_core_v2.rttuple import ATuple, DTuple, FTuple, NtoNTuple, NtoRTuple, NtoCTuple, NtoDETuple, NtoLackRTuple
from rt_core_v2.rttuple_formatter import format_rttuple, json_to_rttuple
from rt_core_v2.metadata_accessory import TupleEventType, RtChangeReason

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
    
ruip = Rui()
ruia = Rui()
ruit= Rui()
ruid = Rui()
ruics = Rui()
ruir = Rui()
ruin = Rui()
ruidt = Rui()

time_1 = TempRef()
event = TupleEventType.INSERT
reason = RtChangeReason.BELIEF
replacements = [ruin, ruidt, ruin]
polarity = False
relation = "part of"
p_list = [ruid, ruin]
time_relation = "at"
code = "code insert"
inst = "instance of"
data = "data insert"

"""Converts the list into a json appropriate representation"""
def jsonify_list(iterable):
    output_str = "["
    for idx, val in enumerate(iterable):
        output_str += '\"'
        output_str += str(val)
        output_str += '\"'
        if idx != len(iterable) -1:
            output_str += ", "

    output_str += "]"
    return output_str

def compare(formatted, expected):
    return ordered(json.loads(formatted)) == ordered(json.loads(expected))

"""All of the below tuple tests first check whether converting from a tuple object to a json functions correclty then checks whether the reverse change is correct."""
def test_atuple_json():
    a = ATuple(ruit, ruia, ruip)
    formatted_a = format_rttuple(a)
    expected_a = f"{{\"ruip\": \"{ruip}\", \"ruia\": \"{ruia}\", \"ruit\": \"{ruit}\", \"type\": \"{a.tuple_type}\", \"unique\": \"{a.unique}\", \"ar\": \"{a.ar}\", \"t\": \"{a.t}\"}}"
    print("Atuple Expected:  \n" + expected_a)
    print("Atuple Processed:  \n" + formatted_a)
    assert compare(formatted_a, expected_a)

    recreated_a = json_to_rttuple(formatted_a)
    print(f"Original ATuple:  {a.get_attributes()}")
    print(f"Recreated ATuple:  {recreated_a.get_attributes()}")
    assert a == recreated_a

def test_dtuple_json():
    d = DTuple(ruid, ruit, time_1, TupleEventType.INSERT, RtChangeReason.BELIEF, replacements)
    formatted_d = format_rttuple(d)
    replacements_repr = jsonify_list(replacements)
    expected_d = f"{{\"type\": \"{d.tuple_type}\", \"ruid\": \"{ruid}\", \"ruit\": \"{ruit}\", \"t\": \"{time_1}\", \"event\": {event}, \"event_reason\": {reason}, \"replacements\": {replacements_repr}}}"
    print("Dtuple Expected:  \n" + expected_d)
    print("Dtuple Processed:  \n" + formatted_d)
    assert compare(formatted_d, expected_d)

    recreated_d = json_to_rttuple(formatted_d)
    print(f"Original DTuple:  {d.get_attributes()}")
    print(f"Recreated DTuple:  {recreated_d.get_attributes()}")
    assert d == recreated_d

def test_ftuple_json():
    C = 0.753
    f = FTuple(ruid, ruit, time_1, ruia, C)
    formatted_f = format_rttuple(f)
    expected_f = f"{{\"type\": \"{f.tuple_type}\", \"ruid\": \"{ruid}\", \"ruit\": \"{ruit}\", \"ta\": \"{time_1}\", \"ruia\": \"{ruia}\", \"C\": {C}}}"
    print("Ftuple Expected:  \n" + expected_f)
    print("Ftuple Processed:  \n" + formatted_f)

    assert compare(formatted_f, expected_f)

    recreated_f = json_to_rttuple(formatted_f)
    print(f"Original FTuple:  {f.get_attributes()}")
    print(f"Recreated FTuple:  {recreated_f.get_attributes()}")
    assert f == recreated_f

def test_nton_json():
    nton = NtoNTuple(ruit, polarity, relation, p_list, time_relation, time_1)
    print(nton.get_attributes())
    formatted_nton = format_rttuple(nton)
    expected_nton = f"{{\"type\": \"{nton.tuple_type}\", \"ruit\": \"{ruit}\", \"polarity\": {str(polarity).lower()}, \"r\": \"{relation}\", \"p\": {jsonify_list(p_list)}, \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\"}}"

    print("Ntontuple Expected:  \n" + expected_nton)
    print("Ntontuple Processed:  \n" + formatted_nton)

    assert compare(formatted_nton, expected_nton)

    recreated_nton = json_to_rttuple(formatted_nton)
    print(f"Original NtonTuple:  {nton.get_attributes()}")
    print(f"Recreated NtonTuple:  {recreated_nton.get_attributes()}")
    
    assert nton == recreated_nton

def test_ntor_json():
    ntor = NtoRTuple(ruit, polarity, inst, ruin, ruir, time_relation, time_1)
    formatted_ntor = format_rttuple(ntor)
    expected_ntor = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntor.tuple_type}\", \"polarity\": {str(polarity).lower()}, \"inst\": \"{inst}\", \"ruir\": \"{ruir}\", \"ruin\": \"{ruin}\", \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\"}}"

    print("Ntortuple Expected:  \n" + expected_ntor)
    print("Ntonrtuple Processed:  \n" + formatted_ntor)

    assert compare(formatted_ntor, expected_ntor)

    recreated_ntor = json_to_rttuple(formatted_ntor)
    print(f"Original NtorTuple:  {ntor.get_attributes()}")
    print(f"Recreated NtorTuple:  {recreated_ntor.get_attributes()}")
    
    assert ntor == recreated_ntor

def test_ntoc_json():
    ntoc = NtoCTuple(ruit, polarity, relation, ruics, ruip, code, time_relation, time_1)
    formatted_ntoc = format_rttuple(ntoc)
    expected_ntoc = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntoc.tuple_type}\", \"polarity\": {str(polarity).lower()}, \"r\": \"{relation}\", \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\", \"ruics\": \"{ruics}\", \"ruip\": \"{ruip}\", \"code\": \"{code}\"}}"

    print("Ntoctuple Expected:  \n" + expected_ntoc)
    print("Ntoctuple Processed:  \n" + formatted_ntoc)

    assert compare(formatted_ntoc, expected_ntoc)

    recreated_ntoc = json_to_rttuple(formatted_ntoc)
    print(f"Original NtocTuple:  {ntoc.get_attributes()}")
    print(f"Recreated NtocTuple:  {recreated_ntoc.get_attributes()}")
    
    assert ntoc == recreated_ntoc

def test_ntode_json():
    ntode = NtoDETuple(ruit, polarity, ruin, data, ruidt)
    formatted_ntode = format_rttuple(ntode)
    expected_ntode = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntode.tuple_type}\", \"polarity\": {str(polarity).lower()}, \"ruin\": \"{ruin}\", \"ruidt\": \"{ruidt}\", \"data\": \"{data}\"}}"

    print("Ntoctuple Expected:  \n" + expected_ntode)
    print("Ntoctuple Processed:  \n" + formatted_ntode)

    assert compare(formatted_ntode, expected_ntode)

    recreated_ntode = json_to_rttuple(formatted_ntode)
    print(f"Original NtodeTuple:  {ntode.get_attributes()}")
    print(f"Recreated NtodeTuple:  {recreated_ntode.get_attributes()}")
    
    assert ntode == recreated_ntode


def test_ntolackr_json():
    ntolackr = NtoLackRTuple(ruit, relation, ruip, ruir, time_relation, time_1)
    formatted_ntolackr = format_rttuple(ntolackr)
    expected_ntolackr = f"{{\"ruit\": \"{ruit}\", \"type\": \"{ntolackr.tuple_type}\", \"r\": \"{relation}\", \"ruir\": \"{ruir}\", \"ruip\": \"{ruip}\", \"tr\": \"{time_1}\", \"rT\": \"{time_relation}\"}}"

    print("Ntortuple Expected:  \n" + expected_ntolackr)
    print("Ntonrtuple Processed:  \n" + formatted_ntolackr)

    assert compare(formatted_ntolackr, expected_ntolackr)

    recreated_ntolackr = json_to_rttuple(formatted_ntolackr)
    print(f"Original NtolackrTuple:  {ntolackr.get_attributes()}")
    print(f"Recreated NtolackrTuple:  {recreated_ntolackr.get_attributes()}")

    assert ntolackr == recreated_ntolackr