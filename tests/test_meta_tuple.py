from rt_core_v2.ids_codes import rui
from rt_core_v2.rttuple import DTuple, FTuple, ATuple
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
        str(dt.td),
    )
    print("\tany replacement tuples: ", dt.replacements)
    print()


def print_f_tuple(ft):
    print(
        "<",
        ft.ruid.uuid,
        "> has confidence level '",
        ft.C,
        "' in tuple <",
        ft.ruitn.uuid,
        "> at ",
        ft.ta,
    )
    print("\ttuple rui: ", ft.rui.uuid)


# create two ATuples with a = rui of person assigning rui to things
a = rui.Rui()
s = rui.Rui()
w = ATuple(a, ruia=a)
x = ATuple(s, ruia=a)

# create two D tuples for each ATuple
# the entity registering the tuples in the RTS
dr = rui.Rui()
# metadata or D tuple for w (ATuple)
dt1 = DTuple(w.rui, rui.TempRef(), TupleEventType.INSERT, RtChangeReason.RELEVANCE, ruid=dr)
# metadata or D tuple for x (ATuple)
dt2 = DTuple(x.rui, rui.TempRef(), TupleEventType.INSERT, RtChangeReason.REALITY, ruid=dr)

print_d_tuple(dt1)
print_d_tuple(dt2)

# now create an FTuple for each ATuple.  ruitn, ruia, ta, C, ruit=None):
# actually at the moment this is a mistake. ATuples won't have associated FTuples. We just need to build the other template types first.
ft1 = FTuple(w.rui, a, rui.TempRef(), rui.Rui(), rui.Rui())
ft2 = FTuple(x.rui, a, rui.TempRef(), rui.Rui(), rui.Rui())
print_f_tuple(ft1)
print_f_tuple(ft2)
