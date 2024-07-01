from uuid6 import uuid7, UUID
from datetime import datetime, timezone
import logging
import enum

class Rui:
	"""Referent Unique Identifier
	A unique identifier for referent tracking

	Attributes:
	status -- the current status of the Rui
	uuid -- the unique identifier of the Rui
	"""

	def __init__(self, uuid: UUID = uuid7()):
		self._uuid = uuid

	@property
	def uuid(self):
		return self._uuid
	
	@uuid.setter
	def uuid(self, uuid):
		self._uuid = uuid

	def __str__(self):
		return str(self._uuid)

#TODO Figure out if the option should be a uuid or an RUI. Probably RUI
class TempRef:
	"""Temporal Reference
	A tuple component that contains is either a calendar date or a unique identifier that represents a instance or interval of time

	Attributes:
	cal -- o
	uuid -- The unique identifier for the tempref
	"""

	def __init__(self, tr, ref_type: str=''):
		self.uuid = None
		self.cal = None
		if (isinstance(tr, datetime)):
			if tr.tzinfo != timezone.utc:
				tr = tr.astimezone(timezone.utc)
			self.cal = tr
		elif (isinstance(tr, UUID)):
			self.uuid = tr
		else:
			if ref_type == 'U':
				self.uuid = uuid7()
			elif ref_type == 'C':
				self.cal = datetime.now(timezone.utc)
			else:
				logging.error("don't understand " + ref_type)
				raise Exception(ref_type + " is not a valid option")

	def isCalendar(self):
		return self.cal

	def isUuid(self):
		return self.uuid
	
	def __str__(self):
		if self.isCalendar():
			return str(self.cal)
		return str(self.uuid)
