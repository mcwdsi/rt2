from abc import ABC, abstractmethod
from typing import Optional

from rt_core_v2.rttuple import RtTuple, TupleType
from rt_core_v2.ids_codes.rui import Rui, TempRef
from rt_core_v2.metadata import RtChangeReason, TupleEventType


class TupleQuery:
    def __init__(
        self,
        types: set[TupleType] = None,
        rui: Optional[Rui] = None,
        author_rui: Optional[Rui] = None,
        relationship_rui: Optional[Rui] = None,
        universal_rui: Optional[Rui] = None,
        begin_timestamp: Optional[TempRef] = None,
        end_timestamp: Optional[TempRef] = None,
        ta: Optional[TempRef] = None,
        tr: Optional[TempRef] = None,
        data: Optional[bytes] = None,
        datatype: Optional[Rui] = None,
        polarity: Optional[bool] = None,
        change_reason: Optional[RtChangeReason] = None,
        change_code: Optional[TupleEventType] = None,
        concept_code: Optional[str] = None,
        confidence: Optional[float] = None,
        p_list: Optional[list[Rui]] = None,
        replacements: Optional[list[Rui]] = None,
        nonrepeatable_rui: Optional[Rui] = None,
        repeatable_rui: Optional[Rui] = None
    ):
        self.types: set[TupleType] = types if types is not None else set()
        self.rui: Optional[Rui] = rui
        self.author_rui: Optional[Rui] = author_rui
        self.relationship_rui: Optional[Rui] = relationship_rui
        self.universal_rui: Optional[Rui] = universal_rui
        self.repeatable_rui: Optional[Rui] = repeatable_rui
        self.nonrepeatable_rui: Optional[Rui] = nonrepeatable_rui
        self.begin_timestamp: Optional[TempRef] = begin_timestamp
        self.end_timestamp: Optional[TempRef] = end_timestamp
        self.ta: Optional[TempRef] = ta
        self.tr: Optional[TempRef] = tr
        self.data: Optional[bytes] = data
        self.datatype: Optional[Rui] = datatype
        self.polarity: Optional[bool] = polarity
        self.change_reason: Optional[RtChangeReason] = change_reason
        self.change_code: Optional[TupleEventType] = change_code
        self.concept_code: Optional[str] = concept_code
        self.confidence: Optional[float] = confidence
        self.p_list: Optional[list[Rui]] = p_list
        self.replacements: Optional[list[Rui]] = replacements

    # Tuples types are filtered out not by the query sharing qualiting that the tuple has, but by the query having any quality that the tuple type does not
    def match_tuple_type(self) -> set[TupleType]:
        """
        Returns a set of all valid tuple types that can be queried based on the current query parameters.
        """
        valid_tuple_types = set()

        if self.match_antuple():
            valid_tuple_types.add(TupleType.AN)
        
        if self.match_artuple():
            valid_tuple_types.add(TupleType.AR)
        
        if self.match_dituple():
            valid_tuple_types.add(TupleType.DI)
        
        if self.match_dctuple():
            valid_tuple_types.add(TupleType.DC)
        
        if self.match_ftuple():
            valid_tuple_types.add(TupleType.F)
        
        if self.match_ntontuple():
            valid_tuple_types.add(TupleType.NtoN)
        
        if self.match_ntortuple():
            valid_tuple_types.add(TupleType.NtoR)
        
        if self.match_ntoctuple():
            valid_tuple_types.add(TupleType.NtoC)
        
        if self.match_ntodetuple():
            valid_tuple_types.add(TupleType.NtoDE)
        
        if self.match_ntolackrtuple():
            valid_tuple_types.add(TupleType.NtoLackR)

        return valid_tuple_types

    def match_antuple(self):
        if self.types and TupleType.AN not in self.types:
            return False
        # ANTuple only has rui, ruia, ruin, ar, unique, and t
        if (
            self.relationship_rui
            or self.data
            or self.change_reason
            or self.datatype
            or self.change_code
            or self.universal_rui
            or self.polarity
            or self.tr
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_artuple(self):
        if self.types and TupleType.AR not in self.types:
            return False
        # ARTuple has ruir, ruio, ar, unique, rui, and t
        if (
            self.relationship_rui
            or self.data
            or self.change_reason
            or self.datatype
            or self.change_code
            or self.polarity
            or self.repeatable_rui
            or self.tr
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_dituple(self):
        if self.types and TupleType.DI not in self.types:
            return False
        # DITuple has ruit, ruid, t, event_reason, ruia, and ta
        if (
            self.data
            or self.datatype
            or self.relationship_rui
            or self.universal_rui
            or self.polarity
            or self.repeatable_rui
            or self.tr
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_dctuple(self):
        if self.types and TupleType.DC not in self.types:
            return False
        # DCTuple has ruit, ruid, t, event, event_reason, and replacements
        if (
            self.data
            or self.datatype
            or self.relationship_rui
            or self.universal_rui
            or self.polarity
            or self.repeatable_rui
            or self.tr
            or self.concept_code
            or self.confidence
            or self.p_list
        ):
            return False
        return True


    def match_ftuple(self):
        if self.types and TupleType.F not in self.types:
            return False
        # FTuple has ruitn, C (confidence level), and t
        if (
            self.relationship_rui
            or self.data
            or self.change_reason
            or self.datatype
            or self.change_code
            or self.universal_rui
            or self.polarity
            or self.repeatable_rui
            or self.tr
            or self.concept_code
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_ntontuple(self):
        if self.types and TupleType.NtoN not in self.types:
            return False
        # NtoNTuple has polarity, r, p_list, tr
        if (
            self.data 
            or self.datatype
            or self.change_reason
            or self.change_code
            or self.universal_rui
            or self.repeatable_rui
            or self.concept_code
            or self.confidence
            or self.replacements
        ):
            return False
        return True

    def match_ntortuple(self):
        if self.types and TupleType.NtoR not in self.types:
            return False
        # NtoRTuple has polarity, r, ruin, ruir, tr
        if (
            self.data
            or self.datatype
            or self.change_reason
            or self.change_code
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_ntoctuple(self):
        if self.types and TupleType.NtoC not in self.types:
            return False
        # NtoCTuple has polarity, r, ruics, ruin, code, tr
        if (
            self.data
            or self.datatype
            or self.change_reason
            or self.change_code
            or self.universal_rui
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_ntodetuple(self):
        if self.types and TupleType.NtoDE not in self.types:
            return False
        # NtoDETuple has polarity, ruin, data, ruidt
        if (
            self.change_reason
            or self.change_code
            or self.universal_rui
            or self.tr
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True

    def match_ntolackrtuple(self):
        if self.types and TupleType.NtoLackR not in self.types:
            return False
        # NtoLackRTuple has r, ruin, ruir, tr
        if (
            self.data
            or self.datatype
            or self.change_reason
            or self.change_code
            or self.concept_code
            or self.confidence
            or self.p_list
            or self.replacements
        ):
            return False
        return True



class RtStore(ABC):
    @abstractmethod
    def save_tuple(self, tup: RtTuple) -> bool:
        pass

    @abstractmethod
    def get_tuple(self, rui: Rui) -> RtTuple:
        pass

    @abstractmethod
    def get_by_referent(self, rui: Rui) -> set[RtTuple]:
        pass

    @abstractmethod
    def get_by_author(self, rui: Rui) -> Rui:
        pass

    @abstractmethod
    def get_available_rui(self) -> Rui:
        pass

    @abstractmethod
    def get_referents_by_type_and_designator_type(self, referent_type: Rui, designator_type: Rui, designator_txt: str) -> set[RtTuple]:
        pass

    @abstractmethod
    def run_query(self, query) -> set[RtTuple]:
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def shut_down(self):
        pass


