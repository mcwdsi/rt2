from rt_core_v2.rttuple import TupleType, DITuple, DCTuple, TupleComponents, RuiStatus, PorType, TempRef, type_to_class
from rt_core_v2.metadata import RtChangeReason, TupleEventType
from rt_core_v2.ids_codes.rui import Rui


def component_to_string(enum_dict):
    return {key.value: val for key, val in enum_dict}

def insert_rttuple(tuple_arguments: dict, type: TupleType):
   return rttuple_factory(tuple_arguments, type, TupleEventType.INSERT, RtChangeReason.RELEVANCE)

# TODO Create support for DTuple author
# TODO Create testing that creates every tuple type using this functions
# TODO Make rttuple_factory insert 
def rttuple_factory(tuple_arguments: dict, type: TupleType, t: TempRef, event: TupleEventType, event_reason: RtChangeReason, replacements: list[Rui], author: Rui):
    # DTuples should only be created in tandem with another tuple
    tuple_arguments = component_to_string(tuple_arguments.items())
    if type in (TupleType.DI, TupleType.DC):
        return None
    try:
        concrete_tuple = type_to_class[type](**tuple_arguments)
        meta_tuple = DITuple(
            concrete_tuple.rui,
            t,
            event_reason, 
            author,
        )
    except TypeError:
        # TODO Log error where tuple has incorrect arguments
        print(f"Incorrect arguments passed for tuple of type {type}")
        return None

    return concrete_tuple, meta_tuple

#TODO Make a factory for each tuple that calls rttuple_factory
def create_antuple(rui: Rui=None, ruia: Rui=None, ruin: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
    antuple_arguments = {TupleComponents.rui:rui, TupleComponents.ruin:ruin, TupleComponents.ar:ar, TupleComponents.unique:unique}
    author = author if author else ruia
    return rttuple_factory(antuple_arguments, TupleType.AN, t, event, event_reason, replacements, author)

def create_ftuple(rui:Rui=None, ruid:Rui=None, ta:TempRef=None, C:float=1.0, ruitn:Rui=None, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
    ftuple_arguments = {TupleComponents.rui:rui, TupleComponents.ruid:ruid, TupleComponents.ta:ta, TupleComponents.ruitn:ruitn, TupleComponents.C:C}
    author = author if author else Rui()
    return rttuple_factory(ftuple_arguments, TupleType.F, t, event, event_reason, replacements, author)

# def create_ntontuple(rui: Rui=None, polarity: bool=True, r: str="", p: list=[], tr: TempRef=None, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
#     nton_arguments = {TupleComponents.rui:rui, TupleComponents.polarity:polarity, TupleComponents.r:r, TupleComponents.p_list:p, TupleComponents.tr:tr}
#     author = author if author else Rui()
#     return rttuple_factory(nton_arguments, TupleType.NtoN, event, event_reason, replacements, author)

# def create_ntortuple(ruit: Rui=None, ruia: Rui=None, ruin: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
#     atuple_arguments = {TupleComponents.rui:ruit, TupleComponents.ruia:ruia, TupleComponents.ruin:ruin, TupleComponents.ar:ar, TupleComponents.unique:unique, TupleComponents.t:t}
#     author = author if author else ruia
#     return rttuple_factory(ntortuple_arguments, TupleType.NtoR, event, event_reason, replacements, author)

# def create_ntodetuple(ruit: Rui=None, ruia: Rui=None, ruin: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
#     atuple_arguments = {TupleComponents.rui:ruit, TupleComponents.ruia:ruia, TupleComponents.ruin:ruin, TupleComponents.ar:ar, TupleComponents.unique:unique, TupleComponents.t:t}
#     author = author if author else ruia
#     return rttuple_factory(ntodetuple_arguments, TupleType.NtoDE, event, event_reason, replacements, author)

# def create_ntoctuple(ruit: Rui=None, ruia: Rui=None, ruin: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
#     atuple_arguments = {TupleComponents.rui:ruit, TupleComponents.ruia:ruia, TupleComponents.ruin:ruin, TupleComponents.ar:ar, TupleComponents.unique:unique, TupleComponents.t:t}
#     author = author if author else ruia
#     return rttuple_factory(ntoctuple_arguments, TupleType.NtoC, event, event_reason, replacements, author)

# def create_ntolackrtuple(ruit: Rui=None, ruia: Rui=None, ruin: Rui=None, ar: RuiStatus=RuiStatus.assigned, unique: PorType=PorType.singular, t: TempRef=None, event=TupleEventType.INSERT, event_reason=RtChangeReason.BELIEF, replacements=[], author=None):
#     atuple_arguments = {TupleComponents.rui:ruit, TupleComponents.ruia:ruia, TupleComponents.ruin:ruin, TupleComponents.ar:ar, TupleComponents.unique:unique, TupleComponents.t:t}
#     author = author if author else ruia
#     return rttuple_factory(ntolackrtuple_arguments, TupleType.NtoLackR, event, event_reason, replacements, author)