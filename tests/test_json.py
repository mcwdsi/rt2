import json

from rt_core_v2.ids_codes.rui import Rui, TempRef, Relationship
from rt_core_v2.rttuple import (
    ANTuple,
    ARTuple,
    DITuple,
    DCTuple,
    FTuple,
    NtoNTuple,
    NtoRTuple,
    NtoCTuple,
    NtoDETuple,
    NtoLackRTuple,
    AttributesVisitor,
)
from rt_core_v2.formatter import format_rttuple, json_to_rttuple
from rt_core_v2.metadata import TupleEventType, RtChangeReason
import base64

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


ruin = Rui()
ruia = Rui()
ruit = Rui()
ruitn = Rui()
ruid = Rui()
ruics = Rui()
ruir = Rui()
ruin = Rui()
ruidt = Rui()
ruio = Rui()
rui = Rui()

get_attributes = AttributesVisitor()

time_1 = TempRef()
event = TupleEventType.REVALIDATE
reason = RtChangeReason.BELIEF
replacements = [ruin, ruidt, ruin]
polarity = False
relation = Rui()
p_list = [ruid, ruin]
code = "code insert"
data_original = "data insert"
data = data_original.encode('utf-8')

"""Converts the list into a json appropriate representation"""


def jsonify_list(iterable):
    output_str = "["
    for idx, val in enumerate(iterable):
        output_str += '"'
        output_str += str(val)
        output_str += '"'
        if idx != len(iterable) - 1:
            output_str += ", "

    output_str += "]"
    return output_str


def compare(formatted, expected):
    return ordered(json.loads(formatted)) == ordered(json.loads(expected))


"""All of the below tuple tests first check whether converting from a tuple object to a json functions correclty then checks whether the reverse change is correct."""


def test_antuple_json():
    a = ANTuple(rui=rui, ruin=ruin)
    formatted_a = format_rttuple(a)
    expected_a = f'{{"ruin": "{ruin}", "rui": "{rui}", "tuple_type": "{a.tuple_type}", "unique": "{a.unique}", "ar": "{a.ar}"}}'
    print("ANtuple Expected:  \n" + expected_a)
    print("ANtuple Processed:  \n" + formatted_a)
    assert compare(formatted_a, expected_a)

    recreated_a = json_to_rttuple(formatted_a)
    print(f"Original ANTuple:  {a.accept(get_attributes)}")
    print(f"Recreated ANTuple:  {recreated_a.accept(get_attributes)}")
    assert a == recreated_a


def test_artuple_json():
    a = ARTuple(rui=rui, ruir=ruir, ruio=ruio)
    formatted_a = format_rttuple(a)
    expected_a = f'{{"rui": "{rui}", "tuple_type": "{a.tuple_type}", "ruir": "{ruir}", "ruio": "{ruio}", "unique": "{a.unique}", "ar": "{a.ar}"}}'
    print("ARtuple Expected:  \n" + expected_a)
    print("ARtuple Processed:  \n" + formatted_a)
    assert compare(formatted_a, expected_a)

    recreated_a = json_to_rttuple(formatted_a)
    print(f"Original ARTuple:  {a.accept(get_attributes)}")
    print(f"Recreated ARTuple:  {recreated_a.accept(get_attributes)}")
    assert a == recreated_a


def test_dituple_json():
    d = DITuple(
        ruit=ruit, t=time_1, event_reason=RtChangeReason.BELIEF, ruid=ruid, rui=rui, ruia=ruia, ta=time_1
    )
    formatted_d = format_rttuple(d)
    expected_d = f'{{"tuple_type": "{d.tuple_type}", "ruid": "{ruid}", "ruit": "{ruit}", "t": "{time_1}", "event_reason": {reason}, "rui": "{rui}", "ruia": "{ruia}", "ta": "{time_1}"}}'
    print("Dtuple Expected:  \n" + expected_d)
    print("Dtuple Processed:  \n" + formatted_d)
    assert compare(formatted_d, expected_d)

    recreated_d = json_to_rttuple(formatted_d)
    print(f"Original DTuple:  {d.accept(get_attributes)}")
    print(f"Recreated DTuple:  {recreated_d.accept(get_attributes)}")
    assert d == recreated_d

def test_dctuple_json():
    d = DCTuple(
        ruit=ruit, t=time_1, event=TupleEventType.REVALIDATE, event_reason=RtChangeReason.BELIEF, ruid=ruid, replacements=replacements, rui=rui
    )
    formatted_d = format_rttuple(d)
    replacements_repr = jsonify_list(replacements)
    expected_d = f'{{"tuple_type": "{d.tuple_type}", "ruid": "{ruid}", "ruit": "{ruit}", "t": "{time_1}", "event": {event}, "event_reason": {reason}, "replacements": {replacements_repr}, "rui": "{rui}"}}'
    print("Dctuple Expected:  \n" + expected_d)
    print("Dctuple Processed:  \n" + formatted_d)
    assert compare(formatted_d, expected_d)

    recreated_d = json_to_rttuple(formatted_d)
    print(f"Original DcTuple:  {d.accept(get_attributes)}")
    print(f"Recreated DcTuple:  {recreated_d.accept(get_attributes)}")
    assert d == recreated_d


def test_ftuple_json():
    C = 0.753
    f = FTuple(ruitn=ruitn, C=C, rui=rui)
    formatted_f = format_rttuple(f)
    expected_f = f'{{"tuple_type": "{f.tuple_type}", "ruitn": "{ruitn}", "C": {C}, "rui": "{rui}"}}'
    print("Ftuple Expected:  \n" + expected_f)
    print("Ftuple Processed:  \n" + formatted_f)

    assert compare(formatted_f, expected_f)

    recreated_f = json_to_rttuple(formatted_f)
    print(f"Original FTuple:  {f.accept(get_attributes)}")
    print(f"Recreated FTuple:  {recreated_f.accept(get_attributes)}")
    assert f == recreated_f


def test_nton_json():
    nton = NtoNTuple(rui=rui, polarity=polarity, r=relation, p=p_list, tr=time_1)
    print(nton.accept(get_attributes))
    formatted_nton = format_rttuple(nton)
    expected_nton = f'{{"tuple_type": "{nton.tuple_type}", "rui": "{rui}", "polarity": {str(polarity).lower()}, "r": "{relation}", "p": {jsonify_list(p_list)}, "tr": "{time_1}"}}'

    print("Ntontuple Expected:  \n" + expected_nton)
    print("Ntontuple Processed:  \n" + formatted_nton)

    assert compare(formatted_nton, expected_nton)

    recreated_nton = json_to_rttuple(formatted_nton)
    print(f"Original NtonTuple:  {nton.accept(get_attributes)}")
    print(f"Recreated NtonTuple:  {recreated_nton.accept(get_attributes)}")

    assert nton == recreated_nton


def test_ntor_json():
    ntor = NtoRTuple(rui=rui, polarity=polarity, r=relation, ruin=ruin, ruir=ruir, tr=time_1)
    formatted_ntor = format_rttuple(ntor)
    expected_ntor = f'{{"rui": "{rui}", "tuple_type": "{ntor.tuple_type}", "polarity": {str(polarity).lower()}, "r": "{relation}", "ruir": "{ruir}", "ruin": "{ruin}", "tr": "{time_1}"}}'

    print("Ntortuple Expected:  \n" + expected_ntor)
    print("Ntonrtuple Processed:  \n" + formatted_ntor)

    assert compare(formatted_ntor, expected_ntor)

    recreated_ntor = json_to_rttuple(formatted_ntor)
    print(f"Original NtorTuple:  {ntor.accept(get_attributes)}")
    print(f"Recreated NtorTuple:  {recreated_ntor.accept(get_attributes)}")

    assert ntor == recreated_ntor


def test_ntoc_json():
    ntoc = NtoCTuple(rui=rui, polarity=polarity, r=relation, ruics=ruics, ruin=ruin, code=code, tr=time_1)
    formatted_ntoc = format_rttuple(ntoc)
    expected_ntoc = f'{{"rui": "{rui}", "tuple_type": "{ntoc.tuple_type}", "polarity": {str(polarity).lower()}, "r": "{relation}", "tr": "{time_1}", "ruics": "{ruics}", "ruin": "{ruin}", "code": "{code}"}}'

    print("Ntoctuple Expected:  \n" + expected_ntoc)
    print("Ntoctuple Processed:  \n" + formatted_ntoc)

    assert compare(formatted_ntoc, expected_ntoc)

    recreated_ntoc = json_to_rttuple(formatted_ntoc)
    print(f"Original NtocTuple:  {ntoc.accept(get_attributes)}")
    print(f"Recreated NtocTuple:  {recreated_ntoc.accept(get_attributes)}")

    assert ntoc == recreated_ntoc


def test_ntode_json():
    ntode = NtoDETuple(rui=rui, polarity=polarity, ruin=ruin, data=data, ruidt=ruidt)
    formatted_ntode = format_rttuple(ntode)
    expected_ntode = f'{{"rui": "{rui}", "tuple_type": "{ntode.tuple_type}", "polarity": {str(polarity).lower()}, "ruin": "{ruin}", "ruidt": "{ruidt}", "data": "{base64.b64encode(data).decode('utf-8')}"}}'
    print("Ntoctuple Expected:  \n" + expected_ntode)
    print("Ntoctuple Processed:  \n" + formatted_ntode)

    assert compare(formatted_ntode, expected_ntode)

    recreated_ntode = json_to_rttuple(formatted_ntode)
    print(f"Original NtodeTuple:  {ntode.accept(get_attributes)}")
    print(f"Recreated NtodeTuple:  {recreated_ntode.accept(get_attributes)}")

    assert ntode == recreated_ntode


def test_ntolackr_json():
    ntolackr = NtoLackRTuple(rui=rui, r=relation, ruin=ruin, ruir=ruir, tr=time_1)
    formatted_ntolackr = format_rttuple(ntolackr)
    expected_ntolackr = f'{{"rui": "{rui}", "tuple_type": "{ntolackr.tuple_type}", "r": "{relation}", "ruir": "{ruir}", "ruin": "{ruin}", "tr": "{time_1}"}}'

    print("Ntortuple Expected:  \n" + expected_ntolackr)
    print("Ntonrtuple Processed:  \n" + formatted_ntolackr)

    assert compare(formatted_ntolackr, expected_ntolackr)

    recreated_ntolackr = json_to_rttuple(formatted_ntolackr)
    print(f"Original NtolackrTuple:  {ntolackr.accept(get_attributes)}")
    print(f"Recreated NtolackrTuple:  {recreated_ntolackr.accept(get_attributes)}")

    assert ntolackr == recreated_ntolackr
