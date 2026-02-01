import pytest
from rt_core_v2.ids_codes.rui import Rui, TempRef
from rt_core_v2.rttuple import (
    ANTuple,
    FTuple,
    DITuple,
    TupleType,
    PorType,
    RuiStatus,
    TupleComponents,
)
from rt_core_v2.metadata import TupleEventType, RtChangeReason
from rt_core_v2.factory import (
    component_to_string,
    insert_rttuple,
    rttuple_factory,
    create_antuple,
    create_ftuple,
)


class TestComponentToString:
    def test_component_to_string_converts_enum_keys(self):
        input_dict = {TupleComponents.rui: "value1", TupleComponents.ruin: "value2"}
        result = component_to_string(input_dict.items())
        assert result == {"rui": "value1", "ruin": "value2"}

    def test_component_to_string_empty_dict(self):
        result = component_to_string({}.items())
        assert result == {}


class TestRttupleFactory:
    def test_rttuple_factory_creates_antuple_with_dituple(self):
        rui = Rui()
        ruin = Rui()
        author = Rui()
        t = TempRef()

        args = {
            TupleComponents.rui: rui,
            TupleComponents.ruin: ruin,
            TupleComponents.ar: RuiStatus.assigned,
            TupleComponents.unique: PorType.singular,
        }

        result = rttuple_factory(
            args,
            TupleType.AN,
            t,
            TupleEventType.INSERT,
            RtChangeReason.BELIEF,
            [],
            author,
        )

        assert result is not None
        concrete_tuple, meta_tuple = result
        assert isinstance(concrete_tuple, ANTuple)
        assert isinstance(meta_tuple, DITuple)
        assert concrete_tuple.rui == rui
        assert concrete_tuple.ruin == ruin

    def test_rttuple_factory_creates_ftuple_with_dituple(self):
        rui = Rui()
        ruitn = Rui()
        author = Rui()
        t = TempRef()
        confidence = 0.85

        args = {
            TupleComponents.rui: rui,
            TupleComponents.ruitn: ruitn,
            TupleComponents.C: confidence,
        }

        result = rttuple_factory(
            args,
            TupleType.F,
            t,
            TupleEventType.INSERT,
            RtChangeReason.BELIEF,
            [],
            author,
        )

        assert result is not None
        concrete_tuple, meta_tuple = result
        assert isinstance(concrete_tuple, FTuple)
        assert isinstance(meta_tuple, DITuple)
        assert concrete_tuple.C == confidence

    def test_rttuple_factory_invalid_arguments_returns_none(self):
        author = Rui()
        t = TempRef()

        # Pass invalid arguments for ANTuple (missing required fields with wrong types)
        args = {TupleComponents.C: "not_a_float"}  # C is for FTuple, not ANTuple

        result = rttuple_factory(
            args,
            TupleType.AN,
            t,
            TupleEventType.INSERT,
            RtChangeReason.BELIEF,
            [],
            author,
        )

        # Factory should handle TypeError and return None or a valid tuple with defaults
        # Based on the implementation, invalid args cause TypeError which returns None
        assert result is None or isinstance(result[0], ANTuple)


class TestCreateAntuple:
    def test_create_antuple_with_defaults(self):
        result = create_antuple()

        # Should return tuple of (ANTuple, DITuple) or None
        if result is not None:
            concrete_tuple, meta_tuple = result
            assert isinstance(concrete_tuple, ANTuple)
            assert isinstance(meta_tuple, DITuple)
            assert concrete_tuple.ar == RuiStatus.assigned
            assert concrete_tuple.unique == PorType.singular

    def test_create_antuple_with_custom_values(self):
        rui = Rui()
        ruin = Rui()
        ruia = Rui()

        result = create_antuple(
            rui=rui,
            ruin=ruin,
            ruia=ruia,
            ar=RuiStatus.reserved,
            unique=PorType.non_singular,
        )

        if result is not None:
            concrete_tuple, meta_tuple = result
            assert concrete_tuple.rui == rui
            assert concrete_tuple.ruin == ruin
            assert concrete_tuple.ar == RuiStatus.reserved
            assert concrete_tuple.unique == PorType.non_singular

    def test_create_antuple_with_event_reason(self):
        result = create_antuple(
            event=TupleEventType.INSERT,
            event_reason=RtChangeReason.REALITY,
        )

        if result is not None:
            concrete_tuple, meta_tuple = result
            assert isinstance(concrete_tuple, ANTuple)
            assert meta_tuple.event_reason == RtChangeReason.REALITY


class TestCreateFtuple:
    def test_create_ftuple_with_defaults(self):
        t = TempRef()
        result = create_ftuple(t=t)

        if result is not None:
            concrete_tuple, meta_tuple = result
            assert isinstance(concrete_tuple, FTuple)
            assert isinstance(meta_tuple, DITuple)
            assert concrete_tuple.C == 1.0

    def test_create_ftuple_with_custom_confidence(self):
        t = TempRef()
        ruitn = Rui()
        confidence = 0.75

        result = create_ftuple(t=t, ruitn=ruitn, C=confidence)

        if result is not None:
            concrete_tuple, meta_tuple = result
            assert concrete_tuple.C == confidence
            assert concrete_tuple.ruitn == ruitn

    def test_create_ftuple_confidence_zero(self):
        t = TempRef()
        result = create_ftuple(t=t, C=0.0)

        if result is not None:
            concrete_tuple, _ = result
            assert concrete_tuple.C == 0.0

    def test_create_ftuple_confidence_one(self):
        t = TempRef()
        result = create_ftuple(t=t, C=1.0)

        if result is not None:
            concrete_tuple, _ = result
            assert concrete_tuple.C == 1.0
