# Victoria Tisdale
# actions.py

from controlflow import GetRDMAction

class GetDeviceInfo(GetRDMAction):
  """An action that GETs DEVICE_INFO."""
  PID = "DEVICE_INFO"

  def ShouldExecute(self):
    """SKip this action if we already have DEVICE_INFO."""
    print self._data
    return self.PID not in self._data

  def UpdateDict(self, succeeded, params):
    if succeeded:
      self._data[self.PID] = params

class GetSupportedParams(GetRDMAction):
	"""
	"""
	self.PID = "SUPPORTED_PARAMETERS"

	def ShouldExecute(self):
		"""" Skip this action if we already have the supported params"""
		return [self.PID] not in self._data

	def UpdateDict(self, succeeded, params):
		if succeeded:
			self._data[self.PID] = ['SUPPORTED_PARAMETERS'] = set(
																				p['param_id'] for p in params['params'])