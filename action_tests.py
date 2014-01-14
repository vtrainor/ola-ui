# Testing functions for OLA_RDM_GUI
# Author: Victoria Tisdale
# Fall 2013

import unittest
import controlflow
import actions
 

def DummyFailedGet(universe, uid, sub_device, pid, callback, data=''):
  # calllback(error, params)
  callback("Simulated Error", None)

def DummyGetDeviceInfo(universe, uid, sub_device, pid, callback, data=''):
  data = {'dmx_footprint': 0, 'software_version': 1, 'personality_count': 4, 
          'device_model': 1, 'current_personality': 1, 'protocol_major': 1, 
          'protocol_minor': 0, 'product_category': 32767, 
          'dmx_start_address': 65535, 'sub_device_count': 0, 'sensor_count': 0
          }
  callback(None, data)
 
def DummyGetParams(universe, uid, sub_device, pid, callback, data=''):
  data = {
      'params': [
          {'param_id': 100},
          {'param_id': 460},
          {'param_id': 971},
      ],
  }
  callback(None, data)

def DummyGetDetailIds(universe, uid, sub_device, pid, callback, data=''):
  data = {
      'detail_ids': [
          {'detail_id': 2306},
          {'detail_id': 32767}
      ]
  }
  callback(None, data)

def DummyGetDeviceModel(universe, uid, sub_device, pid, callback, data=''):
  data = {'description':'Dummy Test Function'}
  callback(None, data)

def DummyGetManufacturer(universe, uid, sub_device, pid, callback, data=''):
  data = {'label': 'Open Lighting Project'}
  callback(None, data)

def DummyGetFactoryDefaults(universe, uid, sub_device, pid, callback, data=''):
  data = {'using_defaults': False}
  callback(None, data)

def DummyGetSoftwareVersion(universe, uid, sub_device, pid, callback, data=''):
  data = {'label': 'OLA Version 0.8.33'}
  callback(None, data)

def DummyGetBootVersion(universe, uid, sub_device, pid, callback, data=''):
  data = {'version': 0xff}
  callback(None, data)

def DummyGetBootLabel(universe, uid, sub_device, pid, callback, data=''):
  data = {'label': 'OLA Boot Version 0.8.33'}
  callback(None, data)
 
class TestBasicInfoGets(unittest.TestCase):
 
  def setUp(self):
    self._universe = 1
    self._uid = 0x7a70ffffffff
    self._callback_run = False
 
  def on_complete(self):
    self._callback_run = True
 
  # ========================== Tests for each action ===========================

  # GetDeviceInfo:
  # def test_failed_get_device_info(self):
  #   # This simulates a failure
  #   data = {}
  #   flow = controlflow.RDMControlFlow(
  #       self._universe,
  #       self._uid,
  #       [ actions.GetDeviceInfo(data, DummyFailedGet) ],
  #       self.on_complete)
  #   flow.run()
 
  #   self.assertTrue(self._callback_run)
  #   self.assertEquals({}, data)

  def test_get_device_info(self):
    # This simulates a success
    data = {}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetDeviceInfo(data, DummyGetDeviceInfo) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {'DEVICE_INFO': {'dmx_footprint': 0, 'software_version': 1, 
        'personality_count': 4, 'device_model': 1, 'current_personality': 1,
        'protocol_major': 1, 'protocol_minor': 0, 'product_category': 32767, 
        'dmx_start_address': 65535, 'sub_device_count': 0, 'sensor_count': 0 }
        }
    self.assertEquals(expected_data, data)

  # GetSupportedParams:
  # def test_failed_get_supported_params(self):
  #   # This simulates a failure
  #   data = {}
  #   flow = controlflow.RDMControlFlow(
  #       self._universe,
  #       self._uid,
  #       [ actions.GetSupportedParams(data, DummyFailedGet) ],
  #       self.on_complete)
  #   flow.run()
 
  #   self.assertTrue(self._callback_run)
  #   self.assertEquals({}, data)

  def test_get_supported_params(self):
    # This simulates a success
    data = {}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetSupportedParams(data, DummyGetParams) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'SUPPORTED_PARAMETERS': set([100, 460, 971]),
    }
    self.assertEquals(expected_data, data)

  # GetProductDetailIds
  def test_get_product_detail_ids(self):
    # This simulates a success
    data = {'PARAM_NAMES': ['PRODUCT_DETAIL_ID_LIST']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetProductDetailIds(data, DummyGetDetailIds) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['PRODUCT_DETAIL_ID_LIST'],
        'PRODUCT_DETAIL_ID_LIST': set([ 2306, 32767]),
    }
    self.assertEquals(expected_data, data)

  # GetDeviceModel
  def test_get_device_model(self):
    data = {'PARAM_NAMES': ['DEVICE_MODEL_DESCRIPTION']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetDeviceModel(data, DummyGetDeviceModel) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['DEVICE_MODEL_DESCRIPTION'],
        'DEVICE_MODEL_DESCRIPTION': 'Dummy Test Function',
    }
    self.assertEquals(expected_data, data)

  # GetManufacturerLabel
  def test_get_manufacturer_label(self):
    data = {'PARAM_NAMES': ['MANUFACTURER_LABEL']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetManufacturerLabel(data, DummyGetManufacturer) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['MANUFACTURER_LABEL'],
        'MANUFACTURER_LABEL': 'Open Lighting Project',
    }
    self.assertEquals(expected_data, data)

  def test_get_factory_defaults(self):
    data = {'PARAM_NAMES': ['FACTORY_DEFAULTS']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetFactoryDefaults(data, DummyGetFactoryDefaults) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['FACTORY_DEFAULTS'],
        'FACTORY_DEFAULTS': False,
    }
    self.assertEquals(expected_data, data)

  def test_get_software_version_label(self):
    data = {}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetSoftwareVersion(data, DummyGetSoftwareVersion) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'SOFTWARE_VERSION_LABEL': 'OLA Version 0.8.33',
    }
    self.assertEquals(expected_data, data)

  def test_get_boot_version(self):
    data = {'PARAM_NAMES': ['BOOT_SOFTWARE_VERSION']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetBootSoftwareVersion(data, DummyGetBootVersion) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['BOOT_SOFTWARE_VERSION'],
        'BOOT_SOFTWARE_VERSION': 0xff,
    }
    self.assertEquals(expected_data, data)

  def test_get_boot_label(self):
    data = {'PARAM_NAMES': ['BOOT_SOFTWARE_LABEL']}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetBootSoftwareLabel(data, DummyGetBootLabel) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
 
    expected_data = {
        'PARAM_NAMES': ['BOOT_SOFTWARE_LABEL'],
        'BOOT_SOFTWARE_LABEL': 'OLA Boot Version 0.8.33',
    }
    self.assertEquals(expected_data, data)

  def test_flow(self):
    data = {'PARAM_NAMES': ['PRODUCT_DETAIL_ID_LIST', 
                            'DEVICE_MODEL_DESCRIPTION',
                            'MANUFACTURER_LABEL',
                            'FACTORY_DEFAULTS',
                            'BOOT_SOFTWARE_VERSION', 
                            'BOOT_SOFTWARE_LABEL',
                           ]
    }
    action_list = [ actions.GetProductDetailIds(data, DummyGetDetailIds),
                    actions.GetDeviceModel(data, DummyGetDeviceModel),
                    actions.GetManufacturerLabel(data, DummyGetManufacturer),
                    actions.GetFactoryDefaults(data, DummyGetFactoryDefaults),
                    actions.GetSoftwareVersion(data, DummyGetSoftwareVersion),
                    actions.GetBootSoftwareVersion(data, DummyGetBootVersion),
                    actions.GetBootSoftwareLabel(data, DummyGetBootLabel)
    ]
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        action_list,
        self.on_complete)
    flow.run()

    self.assertTrue(self._callback_run)

    expected_data = {
        'PARAM_NAMES': ['PRODUCT_DETAIL_ID_LIST', 
                        'DEVICE_MODEL_DESCRIPTION',
                        'MANUFACTURER_LABEL',
                        'FACTORY_DEFAULTS',
                        'BOOT_SOFTWARE_VERSION', 
                        'BOOT_SOFTWARE_LABEL',
                       ],
        'PRODUCT_DETAIL_ID_LIST': set([ 2306, 32767]),
        'DEVICE_MODEL_DESCRIPTION': 'Dummy Test Function',
        'MANUFACTURER_LABEL': 'Open Lighting Project',
        'FACTORY_DEFAULTS': False,
        'SOFTWARE_VERSION_LABEL': 'OLA Version 0.8.33',
        'BOOT_SOFTWARE_VERSION': 0xff,
        'BOOT_SOFTWARE_LABEL': 'OLA Boot Version 0.8.33',
    }
    self.assertEquals(expected_data, data)

def main():
  test = TestBasicInfoGets()
  test.test_flow()  

if __name__ == "__main__":
  unittest.main()