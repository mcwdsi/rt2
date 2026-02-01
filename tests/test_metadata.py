from rt_core_v2.metadata import (
    ValueEnum,
    TupleEventType,
    RtChangeReason,
    pretty_print_dict,
    description_dict,
)


class TestValueEnum:
    def test_value_enum_str_returns_value(self):
        assert str(TupleEventType.INSERT) == "1"
        assert str(TupleEventType.INVALIDATE) == "2"
        assert str(TupleEventType.REVALIDATE) == "3"


class TestTupleEventType:
    def test_tuple_event_type_insert_value(self):
        assert TupleEventType.INSERT.value == 1

    def test_tuple_event_type_invalidate_value(self):
        assert TupleEventType.INVALIDATE.value == 2

    def test_tuple_event_type_revalidate_value(self):
        assert TupleEventType.REVALIDATE.value == 3

    def test_tuple_event_type_all_values_unique(self):
        values = [e.value for e in TupleEventType]
        assert len(values) == len(set(values))

    def test_tuple_event_type_str(self):
        for event_type in TupleEventType:
            assert str(event_type) == str(event_type.value)


class TestRtChangeReason:
    def test_change_reason_belief_value(self):
        assert RtChangeReason.BELIEF.value == 4

    def test_change_reason_reality_value(self):
        assert RtChangeReason.REALITY.value == 5

    def test_change_reason_relevance_value(self):
        assert RtChangeReason.RELEVANCE.value == 6

    def test_change_reason_all_values_unique(self):
        values = [e.value for e in RtChangeReason]
        assert len(values) == len(set(values))

    def test_change_reason_str(self):
        for reason in RtChangeReason:
            assert str(reason) == str(reason.value)

    def test_change_reason_a_type_errors(self):
        """Test A-type error reasons exist"""
        assert RtChangeReason.A1.value == 7
        assert RtChangeReason.A2.value == 8
        assert RtChangeReason.A3.value == 9
        assert RtChangeReason.A4.value == 10

    def test_change_reason_r_type_errors(self):
        """Test R-type error reasons exist"""
        r_types = [
            RtChangeReason.R01, RtChangeReason.R02, RtChangeReason.R03,
            RtChangeReason.R04, RtChangeReason.R05, RtChangeReason.R06,
            RtChangeReason.R07, RtChangeReason.R08, RtChangeReason.R09,
            RtChangeReason.R10,
        ]
        for r_type in r_types:
            assert r_type.value >= 11 and r_type.value <= 20

    def test_change_reason_p_type_errors(self):
        """Test P-type error reasons exist"""
        assert RtChangeReason.P1.value == 21
        assert RtChangeReason.P2.value == 22
        assert RtChangeReason.P3.value == 23

    def test_change_reason_modification_reasons(self):
        """Test modification reasons exist"""
        assert RtChangeReason.AM1.value == 24
        assert RtChangeReason.AM2.value == 25
        assert RtChangeReason.RM1.value == 26
        assert RtChangeReason.RM2.value == 27
        assert RtChangeReason.PM1.value == 28
        assert RtChangeReason.PM2.value == 39  # Note: value is 39, not 29


class TestPrettyPrintDict:
    def test_pretty_print_dict_has_all_event_types(self):
        for event_type in TupleEventType:
            assert event_type in pretty_print_dict, f"Missing {event_type}"

    def test_pretty_print_dict_has_all_change_reasons(self):
        for reason in RtChangeReason:
            assert reason in pretty_print_dict, f"Missing {reason}"

    def test_pretty_print_dict_values_are_strings(self):
        for key, value in pretty_print_dict.items():
            assert isinstance(value, str), f"Value for {key} is not a string"

    def test_pretty_print_dict_values_not_empty(self):
        for key, value in pretty_print_dict.items():
            assert len(value) > 0, f"Value for {key} is empty"


class TestDescriptionDict:
    def test_description_dict_has_all_event_types(self):
        for event_type in TupleEventType:
            assert event_type in description_dict, f"Missing {event_type}"

    def test_description_dict_has_all_change_reasons(self):
        for reason in RtChangeReason:
            assert reason in description_dict, f"Missing {reason}"

    def test_description_dict_values_are_strings(self):
        for key, value in description_dict.items():
            assert isinstance(value, str), f"Value for {key} is not a string"

    def test_description_dict_values_not_empty(self):
        for key, value in description_dict.items():
            assert len(value) > 0, f"Value for {key} is empty"

    def test_description_dict_longer_than_pretty_print(self):
        """Descriptions should generally be more detailed than pretty print"""
        for key in description_dict:
            if key in pretty_print_dict:
                # Most descriptions should be longer or equal
                assert len(description_dict[key]) >= len(pretty_print_dict[key]) - 10
