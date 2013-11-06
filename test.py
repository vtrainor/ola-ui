# Testing functions for OLA_RDM_GUI
# Author: Victoria Tisdale
# Fall 2013

import unittest
import controlflow
import actions
 

def DummyFailedGet(universe, uid, sub_device, pid, callback, data=''):
  # calllback(error, params)
  callback("Simulated Error", None)
 
def DummyGetParams(universe, uid, sub_device, pid, callback, data = {}):
  data = {
      'params': [
          {'param_id': 100},
          {'param_id': 460},
          {'param_id': 971},
      ],
  }
  callback(None, data)
 
 
class TestRDMGetControlFlows(unittest.TestCase):
 
  def setUp(self):
    self._universe = 1
    self._uid = 0x7a70ffffffff
    self._callback_run = False
 
  def on_complete(self):
    self._callback_run = True
 
 
  def test_failed_get_supported_params(self):
    # This simulates a failure
    data = {}
    flow = controlflow.RDMControlFlow(
        self._universe,
        self._uid,
        [ actions.GetSupportedParams(data, DummyFailedGet) ],
        self.on_complete)
    flow.run()
 
    self.assertTrue(self._callback_run)
    self.assertEquals({}, data)
 
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

if __name__ == "__main__":
  unittest.main()