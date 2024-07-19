from rt_core_v2.rttuple import Atuple
from rt_core_v2.ids_codes.Rui import Rui
from datetime import datetime, timezone

def print_atuple(a):
	print("tuple information:")
	print("\truit: the rui that denotes tuple itself", str(a.ruit.uuid))
	print("\truip: rui that was assigned to some PoR", str(a.ruip.uuid))
	print("\tis ruip reserved? ", a.is_reserved())
	print('\tis ruip singularly unique vs. potentially non-singularly unique: ', a.unique)
	print("\truia: rui that denotes person who assigned ruip to some PoR", str(a.ruia.uuid))
	print("\tt: time that ruia assigned/reserved ruip to/for some PoR", str(a.t))
	print()


a = Rui()

x = Rui()
y = Atuple(x)
print_atuple(y)

q = Rui()
z = Atuple(q, ruia=a, unique="+SU", ar='R')
print_atuple(z)

s = Rui()
w = Atuple(s, ruia=a, unique="+SU")
print_atuple(w)

print(type(datetime.now(timezone.utc)))
