import json
import enum

from rttuple import TupleComponents, TupleType, type_to_class

def rttuple_to_json(input_rttuples):
    """Converts either a list or an RtTuple to a json object"""
    return json.dumps(input_rttuples.get_str_attributes())

"""Enum mapping formats to functions to convert RtTuples into the format"""
class RtTupleFormat(enum.Enum):
    json_format = rttuple_to_json

def format_rttuples(tuples, format: RtTupleFormat=RtTupleFormat.json_format):
    """Convert the rttuple to the specified format"""
    return format(tuples)

def json_to_rttuple(tuple_json):
    """Map a json to an rttuple"""
    tuple_dict = json.loads(tuple_json)
    return type_to_class[TupleType(tuple_dict[TupleComponents.type])](**tuple_dict)
