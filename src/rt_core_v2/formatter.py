import json
import enum
from io import StringIO
from uuid import UUID
from datetime import datetime
import base64

from rt_core_v2.rttuple import (
    RtTuple,
    TupleComponents,
    TupleType,
    type_to_class,
    RuiStatus,
    PorType,
    AttributesVisitor,
    RtTupleVisitor,
    ID_Rui, 
    ISO_Rui, 
    UUI,
)
from rt_core_v2.ids_codes.rui import Rui, TempRef, Relationship
from rt_core_v2.metadata import TupleEventType, RtChangeReason


class RtTupleJSONEncoder(json.JSONEncoder):
    """Converts contents of RtTuples into a json representation"""

    str_classes = {Rui, TempRef, PorType, RuiStatus, Relationship, UUI, datetime}
    val_classes = {TupleType, RtChangeReason, TupleEventType,}

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, obj):
        """If the object is an instance of an entry in encoded_classes then convert it to a string for the JSON"""
        if any(isinstance(obj, cls) for cls in self.str_classes):
            return str(obj)
        if any(isinstance(obj, cls) for cls in self.val_classes):
            return obj.value
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        else:
            super().default(obj)

class ToJsonVisitor(RtTupleVisitor):
    """
    Converts an RtTuple into a JSON

    Attributes:
    get_attributes -- Visitor to retrieve a tuple's attributes in a formatted manner
    """
    get_attributes = AttributesVisitor()
    def visit(self, host: RtTuple):
        return json.dumps(host.accept(self.get_attributes), cls=RtTupleJSONEncoder)


# TODO Swap this from an enum to a dictionary
class RtTupleFormat(enum.Enum):
    """A mapping from data represenation formats to functions that perform the conversion on RtTuples"""
    json_format = ToJsonVisitor()


def format_rttuple(tuple: RtTuple, format: RtTupleFormat = RtTupleFormat.json_format):
    """Convert the rttuple to the specified format"""
    return tuple.accept(format.value)


def write_tuples(
    tuples: list[RtTuple],
    stream=StringIO,
    format: RtTupleFormat = RtTupleFormat.json_format,
):
    """Writes all RTtuples to the output stream in the specified format"""
    formatted_tuples = [
        formatted_tuple
        for formatted_tuple in [format_rttuple(tup, format) for tup in tuples]
        if formatted_tuple
    ]
    for tup in formatted_tuples:
        stream.write(tup)


class JsonEntryConverter:
    """Contains functions for converting correclty formatted json representations of tuple fields to tuple fields"""
    format = "%Y-%m-%d %H:%M:%S.%f%z"

    @staticmethod
    def str_to_rui(x: str) -> Rui:
        if ':' in x:
            return JsonEntryConverter.str_to_isorui(x)
        else:
            return JsonEntryConverter.str_to_idrui(x)
    
    @staticmethod
    def str_to_idrui(x: str) -> ID_Rui:
        val = UUID(x)
        return ID_Rui(val)
    
    @staticmethod
    def str_to_isorui(x: str) -> ISO_Rui:
        return ISO_Rui(datetime.strptime(x, JsonEntryConverter.format))
    
    @staticmethod 
    def str_to_uui(x: str) -> UUI:
        return UUI(x)
    
    @staticmethod
    def str_to_relationship(x: str) -> Relationship:
        return Relationship(x)

    @staticmethod
    def lst_to_ruis(x: list[str]) -> list[Rui]:
        return [JsonEntryConverter.str_to_rui(entry) for entry in x]

    @staticmethod
    def str_to_str(x: str):
        return x
    
    @staticmethod
    def process_datetime(x: str):
        return datetime.strptime(x, JsonEntryConverter.format)
    
    @staticmethod
    def process_temp_ref(x: str):
        if ':' in x:
            time_data = JsonEntryConverter.str_to_isorui(x)
        else:
            time_data = JsonEntryConverter.str_to_idrui(x)
        return TempRef(time_data)
    
    @staticmethod
    def str_to_relation(relation_str: str) -> Relationship:
        return Relationship(relation_str)
    
    @staticmethod
    def str_to_bytes(x: str):
        return base64.b64decode(x)



json_entry_converter = {
    TupleComponents.rui: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruin: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruia: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruid: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruir: JsonEntryConverter.str_to_uui,
    TupleComponents.ruics: JsonEntryConverter.str_to_uui,
    TupleComponents.ruidt: JsonEntryConverter.str_to_uui,
    TupleComponents.ruit: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruitn: JsonEntryConverter.str_to_idrui,
    TupleComponents.ruio: JsonEntryConverter.str_to_idrui,
    TupleComponents.t: JsonEntryConverter.process_datetime,
    TupleComponents.ta: JsonEntryConverter.process_temp_ref,
    TupleComponents.tr: JsonEntryConverter.process_temp_ref,
    TupleComponents.ar: lambda x: RuiStatus(x),
    TupleComponents.unique: lambda x: PorType(x),
    TupleComponents.event: lambda x: TupleEventType(x),
    TupleComponents.event_reason: lambda x: RtChangeReason(x),
    TupleComponents.replacements: JsonEntryConverter.lst_to_ruis,
    TupleComponents.p_list: JsonEntryConverter.lst_to_ruis,
    TupleComponents.C: lambda x: float(x),
    TupleComponents.polarity: lambda x: bool(x),
    TupleComponents.r: JsonEntryConverter.str_to_relationship,
    TupleComponents.code: JsonEntryConverter.str_to_str,
    TupleComponents.data: JsonEntryConverter.str_to_bytes,
    TupleComponents.type: lambda x: TupleType(x),
}


def json_to_rttuple(tuple_json) -> RtTuple:
    """Map a json to an rttuple"""
    tuple_dict = json.loads(tuple_json)
    for key, value in tuple_dict.items():
        try:
            entry = TupleComponents(key)
            tuple_dict[key] = json_entry_converter[entry](value)
        except ValueError:
            # TODO Log error
            print(
                f"Invalid rttuple-json processed due to key: {key} with entry: {value}. The processing of this tuple has been skipped."
            )
            return None
    tuple_class = type_to_class[tuple_dict[TupleComponents.type.value]]
    del tuple_dict[TupleComponents.type.value]
    return tuple_class(**tuple_dict)
