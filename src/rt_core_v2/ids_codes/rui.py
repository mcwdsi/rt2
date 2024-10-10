from uuid6 import uuid7, UUID
from typing import Union
from datetime import datetime, timezone

class Rui:
    """Referent Unique Identifier
    A unique identifier for referent tracking

    Attributes:
    uuid -- the unique identifier of the Rui
    """

    def __init__(self, identifier: UUID| str | datetime = None):
        if isinstance(identifier, datetime):
            identifier = identifier.astimezone(timezone.utc)
        self.identifier = identifier if identifier else uuid7()

    @property
    def uuid(self):
        return self.identifier

    @uuid.setter
    def uuid(self, uuid):
        self.identifier = uuid

    def __str__(self):
        return str(self.identifier)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.identifier == other.uuid

    # def __repr__(self):
    #     return self.__str__()


class TempRef:
    """A tuple component that contains is either a calendar date or a unique identifier that represents a instance or interval of time

    Attributes:
    ref -- Identifier for the temporal reference
    """

    def __init__(self, tr: Rui | datetime = None):
        tr = tr if tr else datetime.now()
        if isinstance(tr, datetime):
            tr = tr.astimezone(timezone.utc)
        self.ref = tr

    def __str__(self):
        return str(self.ref)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.ref == other.ref

class Relationship:
    """A tuple component that contains a URI for a relationship

    Attributes:
    uri -- Identifier for the temporal reference
    """
    def __init__(self, uri: str="http://invalid_relationship.com"):
        self.uri = uri

    def __str__(self):
        return str(self.uri)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.__dict__ == other.__dict__

    