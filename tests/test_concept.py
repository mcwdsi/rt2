from rt_core_v2.ids_codes.concept import Concept, Attribute
from rt_core_v2.ids_codes.rui import Rui


class TestConcept:
    def test_concept_initialization(self):
        cs_rui = Rui()
        c = Concept("12345", cs_rui)
        assert c.code == "12345"
        assert c.cs_rui == cs_rui
        assert c.name == ""

    def test_concept_with_optional_name(self):
        cs_rui = Rui()
        c = Concept("12345", cs_rui, "Diabetes Mellitus")
        assert c.code == "12345"
        assert c.cs_rui == cs_rui
        assert c.name == "Diabetes Mellitus"

    def test_concept_attributes_accessible(self):
        cs_rui = Rui()
        c = Concept("ICD10-E11", cs_rui, "Type 2 Diabetes")
        assert hasattr(c, "code")
        assert hasattr(c, "cs_rui")
        assert hasattr(c, "name")

    def test_concept_different_codes(self):
        cs_rui = Rui()
        c1 = Concept("12345", cs_rui)
        c2 = Concept("67890", cs_rui)
        assert c1.code != c2.code

    def test_concept_same_code_different_systems(self):
        cs_rui_1 = Rui()
        cs_rui_2 = Rui()
        c1 = Concept("12345", cs_rui_1)
        c2 = Concept("12345", cs_rui_2)
        assert c1.code == c2.code
        assert c1.cs_rui != c2.cs_rui


class TestAttribute:
    def test_attribute_initialization(self):
        cs_rui = Rui()
        a = Attribute("hasParent", cs_rui)
        assert a.r == "hasParent"
        assert a.cs_rui == cs_rui
        assert a.name == ""

    def test_attribute_with_optional_name(self):
        cs_rui = Rui()
        a = Attribute("hasParent", cs_rui, "Parent Relationship")
        assert a.r == "hasParent"
        assert a.cs_rui == cs_rui
        assert a.name == "Parent Relationship"

    def test_attribute_attributes_accessible(self):
        cs_rui = Rui()
        a = Attribute("partOf", cs_rui, "Part Of Relation")
        assert hasattr(a, "r")
        assert hasattr(a, "cs_rui")
        assert hasattr(a, "name")

    def test_attribute_different_relations(self):
        cs_rui = Rui()
        a1 = Attribute("partOf", cs_rui)
        a2 = Attribute("hasPart", cs_rui)
        assert a1.r != a2.r

    def test_attribute_same_relation_different_systems(self):
        cs_rui_1 = Rui()
        cs_rui_2 = Rui()
        a1 = Attribute("partOf", cs_rui_1)
        a2 = Attribute("partOf", cs_rui_2)
        assert a1.r == a2.r
        assert a1.cs_rui != a2.cs_rui
