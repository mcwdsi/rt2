from uuid6 import uuid7, UUID
from typing import Union
from datetime import datetime, timezone
from abc import ABC, abstractmethod

class Rui(ABC):
    """Referent Unique Identifier (RUI)
    A unique identifier for referent tracking.

    Attributes:
    identifier -- The unique identifier of the Rui.
    """

    @abstractmethod
    def __init__(self, identifier):
        pass

    def __str__(self):
        return str(self.identifier)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.identifier == other.identifier


class ID_Rui(Rui):
    """ID-Based Referent Unique Identifier (RUI)
    A unique identifier based on UUID.

    Attributes:
    identifier -- A UUID that serves as the unique identifier.
    """

    def __init__(self, identifier: UUID = None):
        self.identifier = identifier if identifier else uuid7()

    @property
    def uuid(self):
        return self.identifier

    @uuid.setter
    def uuid(self, uuid):
        self.identifier = uuid


class ISO_Rui(Rui):
    """ISO-Date Based Referent Unique Identifier (RUI)
    A unique identifier based on an ISO 8601 datetime.

    Attributes:
    identifier -- A datetime object representing the ISO-based identifier.
    """

    def __init__(self, identifier: datetime = None):
        identifier = identifier if identifier else datetime.now()
        identifier = identifier.astimezone(timezone.utc)
        self.identifier = identifier

    @property
    def date(self):
        return self.identifier

    @date.setter
    def date(self, date):
        self.identifier = date


class UUI:
    """Universal Unique Identifier (UUI)
    A unique identifier stored as a string.

    Attributes:
    identifier -- A string representing the unique identifier.
    """

    def __init__(self, identifier: str = "http://default_uri.com"):
        self.identifier = identifier

    def __str__(self):
        return str(self.identifier)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.identifier == other.identifier


class TempRef:
    """Temporal Reference (TempRef)
    A tuple component that represents either a calendar date 
    or a unique identifier corresponding to an instance or interval of time.

    Attributes:
    ref -- Identifier for the temporal reference, either a Rui or a datetime.
    """

    def __init__(self, tr: Rui = None):
        self.ref = tr if tr else ID_Rui()

    def __str__(self):
        return str(self.ref)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.ref == other.ref


class Relationship:
    """Relationship Component
    Represents a relationship using a URI.

    Attributes:
    uri -- A string representing the URI of the relationship.
    """

    def __init__(self, uri: str = "http://invalid_relationship.com"):
        self.uri = uri

    def __str__(self):
        return str(self.uri)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__
