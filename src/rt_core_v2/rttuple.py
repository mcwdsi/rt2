import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import ClassVar, override

from rt_core_v2.ids_codes.rui import Rui, UUI, ID_Rui, ISO_Rui, TempRef, Relationship
from rt_core_v2.metadata import TupleEventType, ValueEnum, RtChangeReason
from datetime import datetime, timezone

"""Takes an set of enums and converts them into a dict with mapping entry:value"""


def enum_to_dict(entries: set):
    return {entry: entry.value for entry in entries}


"""Enum representing RUI statuses"""


class RuiStatus(ValueEnum):
    assigned = "A"
    reserved = "R"


"""Enum representing the tuple types"""


class TupleType(ValueEnum):
    AR = "AR"
    AN = "AN"
    DC = "DC"
    DI = "DI"
    F = "F"
    NtoDE = "NtoDE"
    NtoN = "NtoN"
    NtoR = "NtoR"
    NtoC = "NtoC"
    NtoLackR = "NtoLackR"


"""Enum representing portions of reality types"""


class PorType(ValueEnum):
    singular = "+SU"
    non_singular = "-SU"


# TODO Move this into the classes, as it is not a semantically sound placement here
class TupleComponents(enum.Enum):
    ruit = "ruit"
    ruitn = "ruitn"
    ruio = 'ruio'
    type = "tuple_type"
    ar = "ar"
    ruia = "ruia"
    unique = "unique"
    t = "t"
    ruid = "ruid"
    event = "event"
    event_reason = "event_reason"
    replacements = "replacements"
    ta = "ta"
    C = "C"
    polarity = "polarity"
    r = "r"
    p_list = "p"
    tr = "tr"
    ruin = "ruin"
    ruir = "ruir"
    ruics = "ruics"
    code = "code"
    data = "data"
    ruidt = "ruidt"
    rui = "rui"

class RtTupleVisitor(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def visit(self, host):
        pass

class AttributesVisitor(RtTupleVisitor):
    """
    Visitor that converts a tuple's representation to a dictionary 
    mapping the TupleComponent entry type to the value of the entry
    """
    def __init__(self):
        super().__init__()

    @override
    def visit(self, host):
        output = asdict(host)
        for attr_name, attr_value in vars(type(host)).items():
            # Adds class variables, which are attributes that are not callable, private, or already present
            if not callable(attr_value) and not attr_name.startswith("_") and attr_name not in output:
                output[attr_name] = attr_value
        return output


@dataclass
class RtTuple(ABC):
    """Abstract Referent Tracking tuple that contains the information that all referent tracking tuples contain

    Attributes:
    rui -- The rui of this tuple
    type -- The id of the tuple component
    """

    tuple_type: ClassVar[TupleType] = None
    rui: ID_Rui = field(default_factory=ID_Rui)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        get_attr = AttributesVisitor()
        return self.accept(get_attr) == other.accept(get_attr)

    def accept(self, visitor: RtTupleVisitor):
        return visitor.visit(self)

@dataclass(eq=False)
class ANTuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a non-repeatable PoR

    Attributes:
    ar -- The status of ruin - assigned or reserved
    ruin -- The Rui that is being created for the first time
    ruia -- The Rui of the author of this ANTuple
    unique -- Asserts whether this POR is singuarly unique
    t -- The time of the creation of the ANTuple
    """

    tuple_type: ClassVar[TupleType] = TupleType.AN
    ruin: ID_Rui = field(default_factory=ID_Rui)
    ar: RuiStatus = RuiStatus.assigned
    unique: PorType = PorType.singular

@dataclass(eq=False)
class ARTuple(RtTuple):
    """Referent Tracking assignment tuple that registers assignment of an RUI to a repeatable PoR

    Attributes:
    ar -- The status of ruin - assigned or reserved
    ruir -- The ruir that is being created for the first time
    ruio -- The rui of the ontology from which ruir derives
    unique -- Asserts whether this POR is singuarly unique
    t -- The time of the creation of the ARTuple

    Note:
       - We recognize we're getting dangerously close to incorporating ontology development into RT here.
       - It will be a best practice to include an NtoDE with ruin that includes the label of the R POR.
       - We allow IRIs in the UUI type
    """

    tuple_type: ClassVar[TupleType] = TupleType.AR
    ruir: UUI = field(default_factory=UUI)
    ruio: ID_Rui = field(default_factory=ID_Rui)
    ar: RuiStatus = RuiStatus.assigned
    unique: PorType = PorType.singular


@dataclass(eq=False)
class DITuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the insertion of other tuple types into an RT database

    Literally, "metadata (D) for a tuple insertion (I) or DI"

    Attributes:
    ruit -- The rui of the tuple that this metadata tuple is about
    ruid -- The entity who inserted the tuple into the database
    event_reason -- The reason for the event above occuring - e.g., change in reality, relevance, belief, etc.
    t -- The time of this tuple's creation
    ruia -- The author of the tuple that this metadata tuple is about
    ta -- The time of authorship of the tuple that this metadata tuple is about

    We don't have an event_type here because the event_type is implictly tuple insertion based on this metadata tuple type
    """

    # DI#< RUId, RUIT, t, R, RUIa, ta >

    tuple_type: ClassVar[TupleType] = TupleType.DI
    ruit: ID_Rui = field(default_factory=ID_Rui)
    ruid: ID_Rui = field(default_factory=ID_Rui)
    t: datetime = field(default_factory=lambda : datetime.now().astimezone(timezone.utc))
    # The default reason for template insertion is a change in relevance although change in reality will also be common
    event_reason: RtChangeReason = RtChangeReason.RELEVANCE
    # author of the Tuple. Moved from F tuple to here because author might be different from person who expresses confidence level
    ruia: ID_Rui = field(default_factory=ID_Rui)
    # time of tuple authorship. Moved from F tuple to here because time of authorship might be different from time of expressing a confidence level
    ta: TempRef = field(default_factory=TempRef)


@dataclass(eq=False)
class DCTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the change in status of other tuple types such as error correction

    Literally, "metadata (D) for a change in tuple status (C) or DC"

    Attributes:
    ruit -- The rui of another tuple that this tuple stores information about
    ruid -- The rui of the entity making the change in tuple status
    event -- The change made to tuple ruit, either invalidation or revalidation
    event_reason -- The reason for the event above occuring
    t -- The time of this tuple's creation
    replacements -- The ruis of any tuples that ruit replaces
    """

    # D#< RUId, RUIT, t, ‘I’/E, R, S >

    tuple_type: ClassVar[TupleType] = TupleType.DC
    ruit: ID_Rui = field(default_factory=ID_Rui)
    ruid: ID_Rui = field(default_factory=ID_Rui)
    t: datetime = field(default_factory=lambda : datetime.now().astimezone(timezone.utc))
    # The default event for a change in template status is template invalidation although revalidation is also possible
    event: TupleEventType = TupleEventType.INVALIDATE
    # The default reason is R01 which applies only to NtoR tuples, and says that the relationship between ruin and ruir in the NtoR tuple does not hold
    event_reason: RtChangeReason = RtChangeReason.R01
    replacements: list[ID_Rui] = field(default_factory=list)


@dataclass(eq=False)
class FTuple(RtTuple):
    """Referent Tracking metadata tuple that stores information regarding the confidence level in another tuple's assertions

    Note that the time and author of this confidence assertion will be recorded in this F-tuple's associated D-tuple

    Attributes:
    ruitn -- The rui of the tuple that this confidence assertion is about.
    C -- The level of confidence from 0.00-1.00 in the assertion.
    """

    # F#< RUITN, C >

    tuple_type: ClassVar[TupleType] = TupleType.F
    ruitn: ID_Rui = field(default_factory=ID_Rui)
    C: float = 1.0


@dataclass(eq=False)
class NtoNTuple(RtTuple):
    """Tuple type that relates two or more non-repeatable portions of reality to one another

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    relation -- A relation between the non-repeatable portions of reality in p_list
    p_list -- A list of non-repeatable portions of reality that have the relationship described
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoNTuple#< ‘+’/‘-’, r, P, tr/‘-’ >
    tuple_type: ClassVar[TupleType] = TupleType.NtoN
    polarity: bool = True
    r: Relationship = field(default_factory=Relationship)
    p: list[Rui] = field(default_factory=list)
    tr: TempRef = field(default_factory=TempRef)

@dataclass(eq=False)
class NtoRTuple(RtTuple):
    """Tuple type that relates a non-repeatable portion of reality to a repeatable portion of reality

    Attribtues:
    polarity -- Boolean describing whether the relation is as stated or negated
    inst -- The instantiation relationship between the non-repeatable PoR an the repeatable PoR
    ruin -- The Rui of the non-repeatable PoR in the relation
    ruir -- The Rui of the repeatable Por in the relation
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoRTuple#< ‘+’/‘-’, inst, RUIn, RUIr, tr/‘-’ >

    tuple_type: ClassVar[TupleType] = TupleType.NtoR
    polarity: bool = True
    r: Relationship = field(default_factory=Relationship)
    ruin: ID_Rui = field(default_factory=ID_Rui)
    ruir: UUI = field(default_factory=UUI)
    tr: TempRef = field(default_factory=TempRef)


# TODO Use concepts
@dataclass(eq=False)
class NtoCTuple(RtTuple):
    """Tuple type that annotates a non-repeatable portion of reality with a "concept" code from a
    concept-based system

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    relation -- The relationship between the non-repeatable PoR and the concept
    ruics -- The Rui of the concept class the concept for the relation is from
    ruin -- The Rui of the non-repeatable PoR in the relation
    code -- The code for the concept within the concept class referred to by Ruics
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoC#< ‘+’/‘-’, r, RUIcs, ruin, code, tr >

    tuple_type: ClassVar[TupleType] = TupleType.NtoC
    polarity: bool = True
    r: Relationship = field(default_factory=Relationship)
    ruics: UUI = field(default_factory=UUI)
    ruin: ID_Rui = field(default_factory=ID_Rui)
    code: str = ""
    tr: TempRef = field(default_factory=TempRef)


# We use NtoDE instead of NtoI, and we use an instance for the identifying descriptor
# or IdD associated with:
# (1) and NtoRTuple tuple that says what type of IdD it is,
# (2) an NtoNTuple tuple to relate the name to what the IdD denotes, and
# (3) an NtoDE tuple to hold the actual written (or "string") form of the IdD.
# Note that an IdD can be a name, identifier, etc.
@dataclass(eq=False)
class NtoDETuple(RtTuple):
    """Tuple type that creates a connection between a non-repeatable portion of reality and a piece of data

    Attributes:
    polarity -- Boolean describing whether the relation is as stated or negated
    ruin -- The Rui of the tuple that the data is atrributed to
    data -- The data in the relationship
    ruidt -- An Rui containing the data type of data
    """

    # NtoDE#< '+/-', r, ruin, data, ruidt>

    tuple_type: ClassVar[TupleType] = TupleType.NtoDE
    polarity: bool = True
    ruin: ID_Rui = field(default_factory=ID_Rui)
    data: bytes = b''
    #TODO Figure out if this is a uri or a uuid
    ruidt: UUI = field(default_factory=UUI)

@dataclass(eq=False)
class NtoLackRTuple(RtTuple):
    """Tuple type that asserts that a repeatable portion of reality in a does not have a specified relationship with a non-repeateble portion of reality

    Attribtues:
    relation -- A relationship between a non-repeatable portion of reality and a repeatable portion of reality
    ruin -- The rui of the repeatable portion of reality that the non-repeatable does not have the relation to
    ruir -- The rui of the non-repeatable portion fo reality that does not have relation to the POR refered to buy ruin
    time_relation -- The relationship between the time of the creation of this tuple and variable time
    time -- A temporal reference
    """

    # NtoRTuple(-) -tuple NtoRTuple(-)#< r, ruin, RUIr, rT/‘-’, tr/‘-’ >

    tuple_type: ClassVar[TupleType] = TupleType.NtoLackR
    r: Relationship = field(default_factory=Relationship)
    ruin: ID_Rui = field(default_factory=ID_Rui)
    ruir: UUI = field(default_factory=UUI)
    tr: TempRef = field(default_factory=TempRef)

"""Mapping from tuple id to the corresponding tuple class"""
type_to_class = {
    TupleType.AN: ANTuple,
    TupleType.AR: ARTuple,
    TupleType.DI: DITuple,
    TupleType.DC: DCTuple,
    TupleType.F: FTuple,
    TupleType.NtoDE: NtoDETuple,
    TupleType.NtoN: NtoNTuple,
    TupleType.NtoR: NtoRTuple,
    TupleType.NtoC: NtoCTuple,
    TupleType.NtoLackR: NtoLackRTuple,
}