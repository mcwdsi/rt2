from uuid6 import uuid7, UUID

class Rui:
	"""Referent Unique Identifier
	A unique identifier for referent tracking

	Attributes:
	uuid -- the unique identifier of the Rui
	"""

	def __init__(self, uuid: UUID=None):
		self._uuid = uuid if uuid else uuid7()

	@property
	def uuid(self):
		return self._uuid
	
	@uuid.setter
	def uuid(self, uuid):
		self._uuid = uuid

	def __str__(self):
		return str(self._uuid)
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		return self.__dict__ == other.__dict__
	
	def __repr__(self):
		return self.__str__()


class TempRef:
	"""A tuple component that contains is either a calendar date or a unique identifier that represents a instance or interval of time

	Attributes:
	ref -- Identifier for the temporal reference
	"""
	def __init__(self, tr: Rui=None):
		self.ref = tr if tr else Rui()
	
	def __str__(self):
		return str(self.ref)
	
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		return self.__dict__ == other.__dict__

