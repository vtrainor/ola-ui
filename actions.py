# Victoria Tisdale
# actions.py

from controlflow import GetRDMAction
from controlflow import SetRDMAction
from ola import PidStore


class GetDeviceInfo(GetRDMAction):
  """An action that GETs DEVICE_INFO."""
  PID = "DEVICE_INFO"

  def should_execute(self):
    """SKip this action if we already have DEVICE_INFO."""
    print self._data
    return self.PID not in self._data

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetSupportedParams(GetRDMAction):
  """
  """
  PID = "SUPPORTED_PARAMETERS"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return self.PID not in self._data

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = set(p['param_id'] for p in value['params'])

# ==============================================================================
# ============================ Get Basic Info ==================================
# ==============================================================================

class GetProductDetailIds(GetRDMAction):
  PID = "PRODUCT_DETAIL_ID_LIST"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID]= set(
                            data['detail_id'] for data in value['detail_ids'])

class GetDeviceModel(GetRDMAction):
  """
  """
  PID = "DEVICE_MODEL_DESCRIPTION"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["description"]

class GetManufacturerLabel(GetRDMAction):
  """
  """
  PID = "MANUFACTURER_LABEL"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]

class GetFactoryDefaults(GetRDMAction):
  """
  """
  PID = "FACTORY_DEFAULTS"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["using_defaults"]

class GetSoftwareVersion(GetRDMAction):
  """
  """
  PID = "SOFTWARE_VERSION_LABEL"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return self.PID not in self._data

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]

class GetBootSoftwareVersion(GetRDMAction):
  """
  """
  PID = "BOOT_SOFTWARE_VERSION"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["version"]

class GetBootSoftwareLabel(GetRDMAction):
  """
  """
  PID = "BOOT_SOFTWARE_LABEL"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["label"]

# ==============================================================================
# ============================ Get DMX Info ====================================
# ==============================================================================

class GetDmxPersonality(GetRDMAction):
  """
  """
  PID = "DMX_PERSONALITY"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetPersonalityDescription(GetRDMAction):
  """
  """
  PID = "DMX_PERSONALITY_DESCRIPTION"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      index = value["personality"]
      personalities = self._data.setdefault(self.PID, {})
      personalities[index] = {"slots_required":value["slots_required"],
                                     "name":value["name"]}
      

class GetStartAddress(GetRDMAction):
  """
  """
  PID = "DMX_START_ADDRESS"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["dmx_address"]

class GetSlotInfo(GetRDMAction):
  """
  """
  PID = "SLOT_INFO"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      slots = self._data.setdefault(self.PID, {})
      for slot in value["slots"]:
        slots[slot["slot_offset"]] = {
                                      "slot_type": slot["slot_type"],
                                      "slot_label_id": slot["slot_label_id"]
                                     }

class GetSlotDescription(GetRDMAction):
  """
  """
  PID = "SLOT_DESCRIPTION"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

class GetDefaultSlotValue(GetRDMAction):
  """
  """
  PID = "DEFAULT_SLOT_VALUE"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return self.PID in self._data["PARAM_NAMES"]

  def update_dict(self, succeeded, value):
    if succeeded:
      values = self._data.setdefault(self.PID, {})
      for slot_value in value["slot_values"]:
        values[slot_value["slot_offset"]] = slot_value["default_slot_value"]

# ==============================================================================
# ============================ Get Sensors Info ================================
# ==============================================================================

class GetSensorDefinition(GetRDMAction):
  """
  """
  PID = "SENSOR_DEFINITION"
    
  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      index = value['sensor_number']
      sensor_info = self._data.setdefault(self.PID, {})
      sensor_info[index] = value

class GetSensorValue(GetRDMAction):
  """
  """
  PID = "SENSOR_VALUE"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      index = value['sensor_number']
      sensor_info = self._data.setdefault(self.PID, {})
      sensor_info[index] = value

# ==============================================================================
# ============================ Get Setting Info ================================
# ==============================================================================

class GetDeviceHours(GetRDMAction):
  """
  """
  PID = "DEVICE_HOURS"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["hours"]
 
class GetLampHours(GetRDMAction):
  """
  """
  PID = "LAMP_HOURS"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["hours"]

class GetLampStrikes(GetRDMAction):
  """
  """
  PID = "LAMP_STRIKES"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["strikes"]

class GetLampState(GetRDMAction):
  """
  """
  PID = "LAMP_STATE"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["state"]

class GetLampOnMode(GetRDMAction):
  """
  """
  PID = "LAMP_ON_MODE"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["mode"]

class GetPowerCycles(GetRDMAction):
  """
  """
  PID = "DEVICE_POWER_CYCLES"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["power_cycles"]

class GetPowerState(GetRDMAction):
  """
  """
  PID = "POWER_STATE"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["power_state"]

# ==============================================================================
# ============================ Get Config Info =================================
# ==============================================================================

class GetLanguageCapabilities(GetRDMAction):
  """
  """
  PID = "LANGUAGE_CAPABILITIES"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["languages"]

class GetLanguage(GetRDMAction):
  """
  """
  PID = "LANGUAGE"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["language"]

class GetDisplayInvert(GetRDMAction):
  """
  """
  PID = "DISPLAY_INVERT"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["invert_status"]

class GetDisplayLevel(GetRDMAction):
  """
  """
  PID = "DISPLAY_LEVEL"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["level"]

class GetPanInvert(GetRDMAction):
  """
  """
  PID = "PAN_INVERT"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["invert"]

class GetTiltInvert(GetRDMAction):
  """
  """
  PID = "TILT_INVERT"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["invert"]

class GetPanTiltSwap(GetRDMAction):
  """
  """
  PID = "PAN_TILT_SWAP"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value["swap"]

class GetRealTimeClock(GetRDMAction):
  """
  """
  PID = "REAL_TIME_CLOCK"

  def should_execute(self):
    """" Skip this action if we already have the supported params"""
    return (self.PID not in self._data 
                            and self.PID in self._data["PARAM_NAMES"])

  def update_dict(self, succeeded, value):
    if succeeded:
      self._data[self.PID] = value

# ==============================================================================
# ============================ RDM Set Actions =================================
# ==============================================================================

class SetDMXPersonality(SetRDMAction):
  '''
  '''
  PID = 'DMX_PERSONALITY'

  def update_dict(self, succeeded, value):
    if succeeded:
      i = value[0]
      self._data['DEVICE_INFO']['current_personality'] = i
      dmx_footprint = self._data['DMX_PERSONALITY_DESCRIPTION'][i]['slots_required']
      self._data['DEVICE_INFO']['dmx_footprint'] = dmx_footprint
    else:
      print value

class SetSensorValue(SetRDMAction):
  '''
  '''
  PID = 'SENSOR_VALUE'

  def update_dict(self, succeeded, value):
    if succeeded:
      print 'set complete'