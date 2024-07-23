from rt_core_v2.rttuple import TupleType, DTuple, type_to_class
from rt_core_v2.metadata import RtChangeReason, TupleEventType
from rt_core_v2.ids_codes.rui import Rui


def component_to_string(enum_dict):
    return {key.value: val for key, val in enum_dict}

def insert_rttuple(tuple_arguments: dict, type: TupleType):
   return rttuple_factory(dict, type, TupleEventType.INSERT, RtChangeReason.BELIEF)


# TODO Create testing that creates every tuple type using this functions
def rttuple_factory(tuple_arguments: dict, type: TupleType, event: TupleEventType, event_reason: RtChangeReason, replacements: list[Rui]):
    # DTuples should only be created in tandem with another tuple
    tuple_arguments = component_to_string(tuple_arguments)
    if type is TupleType.D:
        return None
    try:
        concrete_tuple = type_to_class[type](**tuple_arguments)
        meta_tuple = DTuple(
            concrete_tuple.ruit,
            concrete_tuple.t,
            event, 
            event_reason, 
            replacements,
        )
    except TypeError:
        # TODO Log error where tuple has incorrect arguments
        print(f"Incorrect arguments passed for tuple of type {type}")
        return None

    return concrete_tuple, meta_tuple

#TODO Make a factory for each tuple that calls rttuple_factory
def create_atuple(ruit: Rui, ruia: Rui, ruip: Rui, ar: , unique, t, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[]):
