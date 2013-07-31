# Victoria Tisdale
# actions.py

from controlflow import GetRDMAction
from ola import PidStore

class GetDeviceInfo(GetRDMAction):
  """An action that GETs DEVICE_INFO."""
  PID = "DEVICE_INFO"

  def ShouldExecute(self):
    """SKip this action if we already have DEVICE_INFO."""
    print self._data
    return self.PID not in self._data

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetSupportedParams(GetRDMAction):
	"""
	"""
	PID = "SUPPORTED_PARAMETERS"

	def ShouldExecute(self):
		"""" Skip this action if we already have the supported params"""
		return self.PID not in self._data

	def UpdateDict(self, succeeded, value):
		if succeeded:
			self._data[self.PID] = set(p['param_id'] for p in value['params'])

class GetDeviceLabel(GetRDMAction):
	"""
	"""
	PID = "DEVICE_LABEL"
		
	def ShouldExecute(self):
		"""" Skip this action if we already have the supported params"""
		pid_key = self._pid_store.GetName(self.PID)
		return (self.PID not in self._data 
														and pid_key in self._data["SUPPORTED_PARAMETERS"])

	def UpdateDict(self, succeeded, value):
		if succeeded:
			self._data[self.PID] = value["label"]