from rt_core_v2.ids_codes.Rui import Rui
from rt_core_v2.rttuple import TupleComponents, TupleType, DTuple, type_to_class
from rt_core_v2.metadata_accessory import RtChangeReason, TupleEventType


#TODO Create testing that creates every tuple type using this function
def rttuple_factory(tuple_arguments: dict, type: TupleType):
    #DTuples should only be created in tandem with another tuple
    if type is TupleType.D:
        return None
    try:
        concrete_tuple = type_to_class[type](**tuple_arguments)
        meta_tuple = DTuple(concrete_tuple.ruit, concrete_tuple.t, TupleEventType.INSERT, RtChangeReason.Belief)
    except TypeError:
        #TODO Log error where tuple has incorrect arguments
        print(f"Incorrect arguments passed for tuple of type {type}")
        return None

    return concrete_tuple, meta_tuple