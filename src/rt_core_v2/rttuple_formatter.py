import json
import enum
from io import StringIO
from uuid import UUID

from rt_core_v2.rttuple import RtTuple, TupleComponents, TupleType, type_to_class, RuiStatus, PorType
from rt_core_v2.ids_codes.Rui import Rui, TempRef
from rt_core_v2.metadata_accessory import TupleEventType, RtChangeReason



class RtTupleJSONEncoder(json.JSONEncoder):
    """Converts contents of RtTuples into a json representation"""
    encoded_classes = {Rui, TempRef, PorType, RuiStatus, TupleType}

    def __init__(self, *args, **kwargs):
        json.JSONEncoder.__init__(self, *args, **kwargs)
    
    def default(self, obj):
        """If the object is an instance of an entry in encoded_classes then convert it to a string for the JSON"""
        if any(isinstance(obj, cls) for cls in self.encoded_classes):
            return str(obj)
        else:
            super().default(obj)


def rttuple_to_json(input_rttuple: RtTuple):
    """Convert an RtTuple to a json object"""
    # return json.dumps(input_rttuple.get_attributes(), default=lambda o: o.toJSON() if hasattr(o, 'toJSON') else str(o))
    return json.dumps(input_rttuple.get_attributes(), cls=RtTupleJSONEncoder)

#TODO Swap this from an enum to a dictionary
class RtTupleFormat(enum.Enum):
    """Enum mapping formats to functions to convert RtTuples into the format"""
    json_format = rttuple_to_json

def format_rttuple(tuple: RtTuple, format: RtTupleFormat=RtTupleFormat.json_format):
    """Convert the rttuple to the specified format"""
    return format(tuple)

def write_tuples(tuples: list[RtTuple], stream=StringIO, format: RtTupleFormat=RtTupleFormat.json_format):
    """Writes all RTtuples to the output stream in the specified format"""
    formatted_tuples= [formatted_tuple for formatted_tuple in [format_rttuple(tup, format) for tup in tuples] if formatted_tuple]
    for tup in formatted_tuples:
        stream.write(tup)

class JsonEntryConverter():
    """Contains functions for converting correclty formatted json representations of tuple fields to tuple fields"""
    @staticmethod
    def str_to_rui(x) -> Rui:
        return Rui(UUID(x))
    
    @staticmethod
    def str_to_temp(x) -> TempRef:
        return TempRef(Rui(UUID(x)))
    
    @staticmethod
    def lst_to_ruis(x) -> list[Rui]:
        return [Rui(UUID(entry)) for entry in x]
    
    @staticmethod
    def str_to_str(x):
        return x

json_entry_converter = {
    TupleComponents.ruit: JsonEntryConverter.str_to_rui,
    TupleComponents.ruip: JsonEntryConverter.str_to_rui,
    TupleComponents.ruia: JsonEntryConverter.str_to_rui,
    TupleComponents.ruid: JsonEntryConverter.str_to_rui,
    TupleComponents.ruin: JsonEntryConverter.str_to_rui,
    TupleComponents.ruir: JsonEntryConverter.str_to_rui,
    TupleComponents.ruics: JsonEntryConverter.str_to_rui,
    TupleComponents.ruidt: JsonEntryConverter.str_to_rui,
    TupleComponents.t: JsonEntryConverter.str_to_temp,
    TupleComponents.td: JsonEntryConverter.str_to_temp,
    TupleComponents.ta: JsonEntryConverter.str_to_temp,
    TupleComponents.tr: JsonEntryConverter.str_to_temp,
    TupleComponents.ar: lambda x: RuiStatus(x),
    TupleComponents.unique: lambda x: PorType(x),
    TupleComponents.event: lambda x: TupleEventType(x),
    TupleComponents.event_reason: lambda x: RtChangeReason(x),
    TupleComponents.replacements: JsonEntryConverter.lst_to_ruis,
    TupleComponents.p_list: JsonEntryConverter.lst_to_ruis,
    TupleComponents.C: lambda x: float(x),
    TupleComponents.polarity: lambda x: bool(x),
    TupleComponents.r: JsonEntryConverter.str_to_str,
    #TODO Figure out type of rT, inst, code, data
    TupleComponents.rT: JsonEntryConverter.str_to_str,
    TupleComponents.inst: JsonEntryConverter.str_to_str,
    TupleComponents.code: JsonEntryConverter.str_to_str,
    TupleComponents.data: JsonEntryConverter.str_to_str,
    TupleComponents.type: lambda x: TupleType(x)
}

def json_to_rttuple(tuple_json) -> RtTuple:
    """Map a json to an rttuple"""
    tuple_dict = json.loads(tuple_json)
    for key, value in tuple_dict.items():
        try:
            entry = TupleComponents(key)
            tuple_dict[key] = json_entry_converter[entry](value)
        except ValueError: 
            #TODO Log error
            print("Invalid rttuple-json processed. The processing of this tuple has been skipped.")
            return None
    tuple_class = type_to_class[tuple_dict[TupleComponents.type.value]]
    del tuple_dict[TupleComponents.type.value]
    return tuple_class(**tuple_dict)

