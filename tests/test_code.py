from rt_core_v2.ids_codes import concept, rui
import sys

sys.path.append("../src")


def print_code(c):
    print("code for concept is", c.code)
    print("\tcode system rui is", str(c.cs_rui.uuid))
    x = c.name
    if x:
        print("\tconcept name is '", x, "'")
    print()


def print_attribute(a):
    print("code for attribute is", a.r)
    print("\tcode system rui is", str(a.cs_rui.uuid))
    y = a.name
    if y:
        print("\tattribute name is '", y, "'")
    print()


csrui = rui.ID_Rui()
c1 = concept.Concept("12345678", csrui)
c2 = concept.Concept("98765432", csrui, "type 2 diabetes mellitus")

print("code 1")
print_code(c1)

print("code 2")
print_code(c2)

a1 = concept.Attribute("456", csrui)
a2 = concept.Attribute("101", csrui, "narrower than")

print_attribute(a1)
print_attribute(a2)
