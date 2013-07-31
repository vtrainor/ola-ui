from collections import deque

class RDMAction(object):
  """The base class all actions inherit from."""
  def Execute(self, on_complete):
    on_complete()

class GetRDMAction(RDMAction):
  """An action which performs an RDM GET."""
  def __init__(self, data_dict, get_fn):
    """Create a new GET action.

    Args:
      data_dict: the dict to update
      get_fn: the function to use for RDM GETs
    """
    self._data = data_dict
    self._get_fn = get_fn

  def Params(self):
    """This method provides the parameters for the GET."""
    return []

  def UpdateDict(succeeded, params):
    """This method is called when the GET completes."""
    pass

  def ShouldExecute(self):
    """This method controls if the action should be skipped."""
    return True

  def Execute(self, universe, uid, on_complete):
    """Perform the RDM GET."""
    if not self.ShouldExecute():
      on_complete()
      return
    self._get_fn(
        universe, uid, 0, self.PID,
        lambda b, s: self._Complete(b, s, on_complete))

  def _Complete(self, succeeded, params, on_complete):
    """Called when the GET completes."""
    self.UpdateDict(succeeded, params)
    on_complete()


class GetIdentify(GetRDMAction):
  """An example GET IDENTIFY_DEVICE action.

  This action always executes, since we want the latest information.
  """
  PID = "IDENTIFY_DEVICE"

  def UpdateDict(self, succeeded, params):
    if succeeded:
      self._data[self.PID] = params['identify_state']

class RDMControlFlow(object):
  """Create a new Control Flow.

  Args:
    universe: the universe to use
    uid: the uid to use
    actions: the list of actions to perform
    on_complete: the method to call when the control flow completes.
  """
  def __init__(self, universe, uid, actions, on_complete):
    self._universe = universe
    self._uid = uid
    self._actions = deque(actions)
    self._on_complete = on_complete

  def Run(self):
    """Run the control flow."""
    self._PerformNextAction()

  def _PerformNextAction(self):
    if self._actions:
      # run next action
      action = self._actions.popleft()
      action.Execute(self._universe, self._uid, self._PerformNextAction)
    else:
      self._on_complete()

# --------------------
# example code

def on_complete():
  print 'control flow completed'

def get_fn(universe, uid, sub_device, pid, callback):
  # This just simulates a RDM GET for now
  print 'GET %s %s %d %s' % (universe, uid, sub_device, pid)
  if pid == 'IDENTIFY_DEVICE':
    callback(True, {'identify_state': True})
  elif pid == 'DEVICE_INFO':
    callback(True, {})
  else:
    callback(False, {})


def test():
  uid = None
  data = {}
  flow = RDMControlFlow(
      1,
      uid,
      [
        GetIdentify(data, get_fn),
        GetDeviceInfo(data, get_fn)

      ],
      on_complete)
  flow.Run()
  print data
	
  print ''
  print 'Running again...'

  flow = RDMControlFlow(
      1,
      uid,
      [
        GetIdentify(data, get_fn),
        GetDeviceInfo(data, get_fn)

      ],
      on_complete)
  flow.Run()

def main():
  test()

if __name__  ==  "__main__":
  main()
