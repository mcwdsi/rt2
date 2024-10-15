from rt_core_v2.ids_codes.rui import Rui, TempRef, ID_Rui
from rt_core_v2.rttuple import (
    ANTuple,
    DITuple,
    DCTuple,
    FTuple,
    NtoNTuple,
    NtoRTuple,
    NtoCTuple,
    NtoDETuple,
    NtoLackRTuple,
    TupleType,
    PorType,
    RuiStatus,
    TupleComponents
)

from rt_core_v2.metadata import TupleEventType, RtChangeReason
from rt_core_v2.factory import insert_rttuple

ruin = ID_Rui()
ruia = ID_Rui()
ruit = ID_Rui()
ruid = ID_Rui()
ruics = ID_Rui()
ruir = ID_Rui()
ruin = ID_Rui()
ruidt = ID_Rui()

unique = PorType.non_singular
ar = RuiStatus.assigned
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


#TODO Fill out tests for tuple factory usage
def test_antuple_factory():
    a = ANTuple(ruit, ruin, ar, unique)
    # a_args = {TupleComponents.ruit:ruit, TupleComponents.ruit:ruia, TupleComponents.ruit:ruin, TupleComponents.ruit:ar, TupleComponents.ruit:unique, TupleComponents.ruit:time_1}
    # a_fac, d_fac = insert_rttuple({:ruit, :ruia, :ruin, :ar, :unique, :time_1}, TupleType.ANTuple)
# def test_dtuple_factory():

# def test_ftuple_factory():

# def test_ntodetuple_factory():

# def test_ntontuple_factory():

# def test_ntortuple_factory():

# def test_ntoctuple_factory():

# def test_ntolackrtuple_factory():

