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
                            and pid_key in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]


# ############################ Get Basic Info ############################

class GetProductDetailIds(GetRDMAction):
  PID = "PRODUCT_DETAIL_ID_LIST"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID]= set(
                            data['detail_id'] for data in value['detail_ids'])

class GetDeviceModel(GetRDMAction):
  """
  """
  PID = "DEVICE_MODEL_DESCRIPTION"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["description"]

class GetManufacturerLabel(GetRDMAction):
  """
  """
  PID = "MANUFACTURER_LABEL"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]

class GetFactoryDefaults(GetRDMAction):
  """
  """
  PID = "FACTORY_DEFAULTS"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["using_defaults"]

class GetSoftwareVersion(GetRDMAction):
  """
  """
  PID = "SOFTWARE_VERSION_LABEL"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]

class GetBootSoftwareVersion(GetRDMAction):
  """
  """
  PID = "BOOT_SOFTWARE_VERSION"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["version"]

class GetBootSoftwareLabel(GetRDMAction):
  """
  """
  PID = "BOOT_SOFTWARE_LABEL"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]


# ############################ Get DMX Info ############################

class GetDmxPersonality(GetRDMAction):
  """
  """
  PID = "DMX_PERSONALITY"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetPersonalityDescription(GetRDMAction):
  """
  """
  PID = "DMX_PERSONALITY_DESCRIPTION"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      index = value["personality"]
      personalities = self._data.setdefault(self.PID, {})
      self._data[self.PID][index] = {"slots_required":value["slots_required"],
                                     "name":value["name"]}
      

class GetStartAddress(GetRDMAction):
  """
  """
  PID = "DMX_START_ADDRESS"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["dmx_address"]

class GetSlotInfo(GetRDMAction):
  """
  """
  PID = "SLOT_INFO"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetSlotDescription(GetRDMAction):
  """
  """
  PID = "SLOT_DESCRIPTION"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetDefaultSlotValue(GetRDMAction):
  """
  """
  PID = "DEFAULT_SLOT_VALUE"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value


# ############################ Get Sensors Info ############################

class GetSensorDefinition(GetRDMAction):
  """
  """
  PID = "SENSOR_DEFINITION"
    
  def ShouldExecute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def UpdateDict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value
#   def _get_sensor_definition(self):
#     pid_key = self._pid_store.GetName("SENSOR_DEFINITION")
#     if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
#           and "SENSOR_DEFINITION" not in self._uid_dict[self.cur_uid]):
#       data = [1]
#       self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
#             lambda b, s: self._get_sensor_definition_complete(b, s), data)
#     else:
#       self._get_sensor_value()

#   def _get_sensor_definition_complete(self, succeeded, data):
#     if succeeded:
#       print ""
#       self._uid_dict[self.cur_uid]["SENSOR_DEFINITION"] = data
#     else:
#       print "failed"
#     # store the results in the uid dict
#     self._get_sensor_value()

#   def _get_sensor_value(self):
#     pid_key = self._pid_store.GetName("SENSOR_VALUE")
#     if (pid_key.value in self._uid_dict[self.cur_uid]['SUPPORTED_PARAMETERS']
#           and "SENSOR_VALUE" not in self._uid_dict[self.cur_uid]):
#       data = [1]
#       self.ola_thread.rdm_get(self.universe.get(), self.cur_uid, 0, pid_key.name, 
#             lambda b, s: self._get_sensor_value_complete(b, s), data)
#     else:
#       self._notebook.RenderSensorInformation(self._uid_dict[self.cur_uid])
#       # do I need to do anything with record sensors here?

#   def _get_sensor_value_complete(self, succeeded, data):
#     if succeeded:
#       print ""
#       self._uid_dict[self.cur_uid]["SENSOR_VALUE"] = data
#     else:
#       print "failed"
#     # store the results in the uid dict
#     self._notebook.RenderSensorInformation(self._uid_dict[self.cur_uid])
#     print "sensor value"

# # ############################ Get Setting Info ############################

# # ############################ Get Config Info ############################
