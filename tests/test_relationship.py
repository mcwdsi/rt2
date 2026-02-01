from rt_core_v2.ids_codes.rui import Relationship


def test_relationship_default_uri():
    r = Relationship()
    assert r.uri == "http://invalid_relationship.com"


def test_relationship_custom_uri():
    uri = "http://example.org/partOf"
    r = Relationship(uri)
    assert r.uri == uri


def test_relationship_equality_same_uri():
    uri = "http://example.org/partOf"
    r1 = Relationship(uri)
    r2 = Relationship(uri)
    assert r1 == r2


def test_relationship_equality_different_uri():
    r1 = Relationship("http://example.org/partOf")
    r2 = Relationship("http://example.org/hasPart")
    assert r1 != r2


def test_relationship_equality_non_relationship():
    r = Relationship("http://example.org/partOf")
    assert r != "http://example.org/partOf"
    assert r != None
    assert r != 42


def test_relationship_str_representation():
    uri = "http://example.org/partOf"
    r = Relationship(uri)
    assert str(r) == uri


def test_relationship_str_default():
    r = Relationship()
    assert str(r) == "http://invalid_relationship.com"
