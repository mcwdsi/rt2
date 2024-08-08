from abc import ABC, abstractmethod
from typing import Optional

from rt_core_v2.rttuple import RtTuple, TupleType, TupleComponents
from rt_core_v2.ids_codes.Rui import Rui, TempRef
from rt_core_v2.metadata_accessory import RtChangeReason, TupleEventType

#TODO Change fields to be up to date with referent tracking 2.0 
class TupleQuery():
    def __init__(self):
        self.types: set[TupleType] = set()
        self.rui: Optional[Rui] = None
        self.relationship_rui: Optional[Rui] = None
        self.universal_rui: Optional[Rui] = None
        self.author_rui: Optional[Rui] = None
        self.authoring_time_rui: Optional[Rui] = None
        self.begin_timestamp: Optional[TempRef] = None
        self.end_timestamp: Optional[TempRef] = None
        self.data: Optional[bytes] = None
        self.datatype: Optional[Rui] = None
        self.change_reason: Optional[RtChangeReason] = None
        self.error_code: Optional[TupleEventType] = None
        self.temporal_entity_name: Optional[str] = None
        self.tr: Optional[TempRef] = None
        #TODO Figure out particular reference type for self.p
        self.p: Optional[Rui] = None
        self.polarity: Optional[bool] = None

    #TODO Make this general
    # def parameters_match_tuple(self, tuple_type):
    
    def match_atuple(self):
        if self.types and TupleType.A not in self.types:
            return False
        if self.relationship_rui or self.data or self.change_reason or self.datatype or self.error_code or self.temporal_entity_name or self.universal_rui or self.polarity:
            return False
        return True
    
    def match_dtuple(self):
        if self.types and TupleType.D not in self.types:
            return False
        if self.data or self.datatype or self.temporal_entity_name or self.relationship_rui or self.universal_rui or self.polarity:
            return False
        return True
    
    #TODO Fill out ftuple match
    def match_ftuple(self):
        if self.types and TupleType.F not in self.types:
            return False
        return True
    
    def match_ntontuple(self):
        if self.types and TupleType.NtoNTuple not in self.types:
            return False
        if self.datatype or self.change_reason or self.error_code or self.temporal_entity_name or self.universal_rui:
            return False
        return True
    
    def match_ntortuple(self):
        if self.types and TupleType.NtoRTuple not in self.types:
            return False
        if self.data or self.datatype or self.change_reason or self.error_code or self.temporal_entity_name:
            return False
        return True
    
    #TODO Fill out ntoc tuple
    def match_ntoctuple(self):
        if self.types and TupleType.NtoC not in self.types:
            return False
        return True
    
    #TODO Fill out ntode tuple
    def match_ntodetuple(self):
        if self.types and TupleType.NtoDE not in self.types:
            return False
        return True
    
    def ntolackrtuple(self):
        if self.types and TupleType.NtoLackR not in self.types:
            return False
        if self.data or self.datatype or self.change_reason or self.error_code or self.temporal_entity_name or self.polarity:
            return False
        return True

class RtStore(ABC):

    @abstractmethod
    def save_tuple(self, tup: RtTuple) -> bool:
        pass

    @abstractmethod
    def get_tuple(self, tup: RtTuple) -> Rui:
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
    def get_by_type(self, referentType, designatorType, designatorText) -> set:
        pass

    @abstractmethod
    def run_query(self, query) -> set[RtTuple]:
        pass

    @abstractmethod
    def shut_down(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def save_rts_declaration(self, declaration) -> bool:
        pass
