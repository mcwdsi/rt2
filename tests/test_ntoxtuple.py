from rt_core_v2.ids_codes import rui
from rt_core_v2.rttuple import ANTuple, NtoRTuple, NtoNTuple, RuiStatus


def print_ANTuple(a):
    print("AN tuple information:")
    print("\trui: the rui that denotes tuple itself", str(a.rui.uuid))
    print("\truin: rui that was assigned to some PoR", str(a.ruin.uuid))
    print("\tis ruin reserved? ", a.ar)
    print(
        "\tis ruin singularly unique vs. potentially non-singularly unique: ", a.unique
    )
    print()


def print_NtoRTuple_tuple(NtoRTuple):
    print("NtoRTuple tuple information:")
    print(
        "\trui: the rui that the system assigned to the NtoRTuple tuple itself --",
        str(NtoRTuple.rui.uuid),
    )
    print(
        "\truin: the rui that denotes the non-repeatable PoR that this tuple is about --",
        str(NtoRTuple.ruin.uuid),
    )
    print(
        "\truir: the rui that denotes the repeatable PoR to which the non-repeatable PoR (denoted by ruinI) is related --",
        NtoRTuple.ruir.uuid,
    )
    print(
        "\tr: the relationship between the non-repeatable PoR and the repeatable PoR --",
        str(NtoRTuple.r),
    )
    print(
        "\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --",
        str(NtoRTuple.tr.ref),
    )
    print(
        "\tpolarity: the relationship holds (true) or does not hold (false) --",
        str(NtoRTuple.polarity),
    )
    print()


def print_NtoNTuple_tuple(NtoNTuple):
    print("NtoNTuple tuple information:")
    print(
        "\trui: the rui that the system assigned to the NtoRTuple tuple itself --",
        str(NtoNTuple.rui.uuid),
    )
    print(
        "\tP: the list of ruis that denote the non-repeatable PoRs that are related by r:"
    )
    for i in NtoNTuple.p:
        print("\t\t", i.uuid)
    print(
        "\tr: the relationship between the non-repeatable PoR and the repeatable PoR --",
        str(NtoNTuple.r),
    )
    print(
        "\ttr: the time at which the relationship between the non-repeatable PoR and the repeatable PoR holds --",
        str(NtoNTuple.tr.ref),
    )
    print(
        "\tpolarity: the relationship holds (true) or does not hold (false) --",
        str(NtoNTuple.polarity),
    )
    print()


# Rui that represents the person authoring these tuples
a = rui.ID_Rui()
# Rui that stands for the repeatable PoR called "human being"
h = rui.ID_Rui()
# Rui that stands for interval over which author has been instance of human being
tr1 = rui.ID_Rui()
k = ANTuple(tr1)

NtoRTuple = NtoRTuple(polarity=True, r="part of", ruin=a, ruir=h, tr=rui.TempRef())
print_NtoRTuple_tuple(NtoRTuple)

# let x be the RUI standing for Kuala Lumpur
x = rui.ID_Rui()
y = ANTuple(x)
print_ANTuple(y)

q = rui.ID_Rui()
z = ANTuple(q, ar=RuiStatus.reserved)
print_ANTuple(z)

# let s be the RUI standing for the territory of Malaysia
s = rui.ID_Rui()
w = ANTuple(s)
print_ANTuple(w)

# let tr2 be interval over which kuala lumpur has been part of Malaysia
tr2 = rui.ID_Rui()
j = ANTuple(tr2)
NtoNTuple = NtoNTuple(polarity=True, r="part of", p=[x, s], tr=rui.TempRef())
print_NtoNTuple_tuple(NtoNTuple)
