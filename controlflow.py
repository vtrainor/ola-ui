from collections import deque

class RDMAction(object):
  """The base class all actions inherit from."""
  def Execute(self, on_complete):
    on_complete()

class GetRDMAction(RDMAction):
  """An action which performs an RDM GET."""
  def __init__(self, data_dict, get_fn, get_data = []):
    """Create a new GET action.

    see actions.py for examples of child classes.

    Args:
      data_dict: the dict to update
      get_fn: the function to use for RDM GETs
    """
    self._data = data_dict
    self._get_fn = get_fn
    self._get_data = get_data

  def update_dict(self, error, value):
    """This method is called when the GET completes.

    action child classes should define this method for the UI to access the
    information
    """
    pass

  def should_execute(self):
    """This method controls if the action should be skipped.

    Unless redefined in a child class this method will always execute the
    action.
    """
    return True

  def pid_supported(self):
    """ Test whether or not the PID is supported by the current device.

    Returns:
      A boolean value that is True when the PID is supported by the current
      device and False when the PID is not.
    """
    return self.PID in self._data['PARAM_NAMES']

  def execute(self, universe, uid, on_complete):
    """Perform the RDM GET.

    Tests whether or not the action should be executed. If not, calls the next 
    function in the control flow.

    Args:
      universe: int, the current DMX universe
      uid: UID object, the UID for the currently selected device
      on_complete: lambda function, the next function in the control 
    """
    if not self.should_execute():
      on_complete()
      return
    self._get_fn(
        universe, uid, 0, self.PID,
        lambda b, s: self._complete(b, s, on_complete),
        self._get_data)

  def _complete(self, error, value, on_complete):
    """Called when the GET completes.

    Calls update_dict for this action and then the next function in the control
    flow

    Args:
      error: if the RDM get fails, value of the error the cause the RDM call to
        fail.
      value: the RDM get response
      on_complete: lamda function, next call in the control flow
    """
    self.update_dict(error, value)
    on_complete()

class SetRDMAction(RDMAction):
  """An action which performs an RDM GET."""
  def __init__(self, data_dict, set_fn, set_data = []):
    """Create a new GET action.

    Args:
      data_dict: the dict to update
      get_fn: the function to use for RDM GETs
    """
    self._data = data_dict
    self._set_fn = set_fn
    self._set_data = set_data

  def update_dict(succeeded, params):
    """This method is called when the SET completes.

    Needs to be redefined in the child class for the UI to access the RDM
    information.
    """
    pass

  def should_execute(self):
    """This method controls if the action should be skipped.

    Always returns True, unless the method is redefined in the child class
    """
    return True

  def execute(self, universe, uid, on_complete):
    """Perform the RDM GET.

    Args:
      universe: the current DMX universe
      uid: the UID for the currently selected device
      on_complete:
    """
    if not self.should_execute():
      on_complete()
      return
    self._set_fn(
        universe, uid, 0, self.PID,
        lambda b, s: self._complete(b, s, on_complete),
        self._set_data)

  def _complete(self, error, value, on_complete):
    """Called when the GET completes.

    Args:
      error: if the RDM call succeeded this value is None, otherwise it will be
        a string value of the error that caused the failure in the ola thread. 
        will be displayed in dialog window
      value: if the RDM call fails this value will be None, Otherwise it will be
        the value returned by the RDM set.
    """
    self.update_dict(error, self._set_data)
    on_complete()

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

  def run(self):
    """Run the control flow."""
    self._perform_next_action()

  def _perform_next_action(self):
    if self._actions:
      action = self._actions.popleft()
      action.execute(self._universe, self._uid, self._perform_next_action)
    else:
      self._on_complete()