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

