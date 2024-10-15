from rt_core_v2.ids_codes import rui
from rt_core_v2.rttuple import DCTuple, FTuple, ANTuple
from rt_core_v2.metadata import TupleEventType, RtChangeReason


# print functions
def print_d_tuple(dt):
    print(
        "<",
        dt.rui.uuid,
        "> did a(n) ",
        dt.event,
        " to tuple <",
        dt.ruit.uuid,
        "> because of ",
        dt.event_reason,
        " at ",
        str(dt.t),
    )
    print("\tany replacement tuples: ", dt.replacements)
    print()


def print_f_tuple(ft):
    print(
        "confidence level '",
        ft.C,
        "' in tuple <",
        ft.ruitn.uuid,
    )
    print("\ttuple rui: ", ft.rui.uuid)


# create two ANTuples with a = rui of person assigning rui to things
a = rui.ID_Rui()
s = rui.ID_Rui()
w = ANTuple(a)
x = ANTuple(s)

# create two D tuples for each ANTuple
# the entity registering the tuples in the RTS
dr = rui.ID_Rui()
# metadata or D tuple for w (ANTuple)
dt1 = DCTuple(ruid=a, ruit=a, event=TupleEventType.INSERT, event_reason=RtChangeReason.REALITY)
# metadata or D tuple for x (ANTuple)
dt2 = DCTuple(ruid=a, ruit=s, event=TupleEventType.INSERT, event_reason=RtChangeReason.REALITY)

print_d_tuple(dt1)
print_d_tuple(dt2)

# now create an FTuple for each ANTuple.  ruitn, ruia, ta, C, ruit=None):
# actually at the moment this is a mistake. ANTuples won't have associated FTuples. We just need to build the other template types first.
ft1 = FTuple(ruitn=w.rui, C=0.76)
ft2 = FTuple(ruitn=x.rui, C=0.5)
print_f_tuple(ft1)
print_f_tuple(ft2)
