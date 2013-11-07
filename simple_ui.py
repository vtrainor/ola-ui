import Tkinter as tk
from ola.ClientWrapper import ClientWrapper
import time
import threading
import thread
import Queue
import olathread
from ola import PidStore
import ttk
import notebook
import controlflow
import actions
import logging
from rdm_menu import RDMMenu
from rdm_dialog import RDMDialog
import PIDDict

'''
 General control flow:

 On startup:
   - fetch the list of UIDS
   - for each UID, fetch the DEVICE_LABEL
   - add each UID & add UID (+ optional label) to the drop down

 When a UID is selected:
  - fetch supported params if we don't already have it
  - fetch device info if we don't already have it
  - call notebook.update()
  - notebook.update looks at the current selected tab, and then calls one of:
    - get_basic_information()
    - get_dmx_information()
    - GetSensorInformation()

 Each of these send the necessary to build a dictionary (pid_info) for the tab.
 For example, get_basic_information() would do:
    GET PRODUCT_DETAIL_ID_LIST
    GET -PRODUCT_DETAIL_ID_LIST
    GET MANUFACTURER_LABEL
    GET SOFTWARE_VERSION_LABEL
    GET BOOT_SOFTWARE_VERSION_ID
    GET BOOT_SOFTWARE_VERSION_LABEL

  Once the dict is built, we call notebook.render_basic_information(pid_info)
  which then updates all the widgets.
'''

# ==============================================================================
# ============================ Controller Class ================================
# ==============================================================================

class Controller(object):
  '''The controller will act as the glue between the notebook (display) the the
     DisplayApp (data). This keeps us honest by not leaking RDM information
     into the notebook.
  '''
  def __init__(self, app):
    self._app = app

  def get_basic_information(self):
    self._app.get_basic_information()

  def get_dmx_information(self):
    self._app.get_dmx_information()

  def get_sensor_value(self, sensor_number):
    self._app.get_sensor_value(sensor_number)

  def get_sensor_definitions(self):
    self._app.get_sensor_definitions()

  def get_setting_information(self):
    self._app.get_setting_information()

  def get_config_information(self):
    self._app.get_config_information()

  def set_device_label(self, label):
    self._app.set_device_label(label)

  def set_start_address(self, start_address):
    self._app.set_start_address(start_address)

  def set_dmx_personality(self, index):
    self._app.set_dmx_personality(index)

  def set_lamp_state(self, state):
    self._app.set_lamp_state(state)

  def set_lamp_on_mode(self, mode):
    self._app.set_lamp_on_mode(mode)

  def set_power_state(self, state):
    self._app.set_power_state(state)

  def set_language(self, language):
    self._app.set_language(language)

  def set_display_invert(self, invert):
    self._app.set_display_invert(invert)

  def set_display_level(self, level):
    self._app.set_display_level(level)

  def set_pan_invert(self, invert):
    self._app.set_pan_invert(invert)

  def set_tilt_invert(self, invert):
    self._app.set_tilt_invert(invert)

  def set_pan_tilt_swap(self, swap):
    self._app.set_pan_tilt_swap(swap)

  def record_sensor(self, sensor_number):
    self._app.record_sensor(sensor_number)

  def clear_sensor(self, sensor_number):
    self._app.clear_sensor(sensor_number)

# ==============================================================================
# ============================ Universe Class ==================================
# ==============================================================================
class UniverseObj(object):
  ''' The UniverseObj class is used to access infromation for each Universe as
      the user fetches new universes or switches between Universes in the GUI
  '''

  def __init__(self, uni_id, name):
    self._id = uni_id 
    self._name = name 
    self._discover = False
    self._uids = set()

  @property
  def name(self):
    return self._name

  @property
  def id(self):
    return self._id

  @property
  def discovery_run(self):
    return self._discover

  @property
  def uids(self):
    return self._uids

  def set_uids(self, uid_list):
    self._uids = set(uid_list)
    self._discover = True


# ==============================================================================
# ============================ Display App Class ===============================
# ==============================================================================

class DisplayApp(object):
  ''' Creates the GUI for sending and receiving RDM messages through the
      ola thread. 
  '''
  def __init__(self, width, height):
    ''' initializes the GUI and the ola thread
    
    Args:
      width: the int value of the width of the tkinter window
      height: the int value of the height of the tkinter window
    '''
    # ================== Initialize the tk root window =========================
    self._controller = Controller(self)
    self.root = tk.Tk()
    self.init_dx = width
    self.init_dy = height
    self.root.geometry('%dx%d+50+30'%(self.init_dx, self.init_dy))
    self.root.title('RDM user interface version: 1.0')
    self.root.maxsize(1600, 900)
    self.root.lift()
    self.root.update_idletasks()
    # ================== Initialize Variables and Ola Thread ===================
    self.universe = tk.IntVar(self.root)
    self.universe_dict = {}
    self._cur_uid = None
    self._uid_dict = {}
    self._pid_store = PidStore.GetStore()
    self.ola_thread = olathread.OLAThread(self._pid_store)
    self.ola_thread.start()
    self.build_frames()
    self.build_cntrl()
    self._notebook = notebook.RDMNotebook(self.root, self._controller)
    # ================== Call Fetch Universes ==================================
    self.fetch_universes(self.fetch_universes_complete)

    print 'currently in thread: %d' % threading.currentThread().ident
    time.sleep(1)
    print 'back from sleep'


  def build_frames(self):
    ''' builds the two tkinter frames that are used as parents for the
       tkinter widgets that both control and display the RDM messages.
    '''
    self.cntrl_frame = tk.PanedWindow(self.root)
    self.cntrl_frame.pack(side = tk.TOP, padx = 1, pady = 1, fill = tk.Y)
    self.info_frame_1 = tk.PanedWindow(self.root)
    self.info_frame_1.pack(side = tk.TOP, padx = 1, pady = 2, fill = tk.Y)
    
  def build_cntrl(self):
    ''' Builds the top bar of the GUI.

    Initializes all the general tkinter control widgets
    '''
    tk.Label(self.cntrl_frame, text = 'Select\nUniverse:').pack(side = tk.LEFT)
    self.universe_menu = RDMMenu(self.cntrl_frame, 'No Universes Available',
                                  'Select Universe')
    self.universe_menu.pack(side = tk.LEFT)
    discover_button = tk.Button(self.cntrl_frame, text = 'Discover', 
                                command = self.discover)
    discover_button.pack(side = tk.LEFT)
    self.device_menu = RDMMenu(self.cntrl_frame, "No Devices", "Select Device")
    self.device_menu.pack(side = tk.LEFT)
    self.id_state = tk.IntVar(self.root)
    self.id_state.set(0)
    self.id_box = tk.Checkbutton(self.cntrl_frame, text = 'Identify', 
                                 variable = self.id_state, 
                                 command = self.identify)
    self.id_box.pack(side = tk.LEFT)
    self.auto_disc = tk.BooleanVar(self.root)
    self.auto_disc.set(False)
    self.auto_disc_box = tk.Checkbutton(self.cntrl_frame, 
                                        text = 'Automatic\nDiscovery',
                                        variable = self.auto_disc, 
                                        command = self.discover)
    self.auto_disc_box.pack(side = tk.LEFT)

  def device_selected(self, uid):
    ''' called when a new device is chosen from dev_menu.

      Args: 
        uid: the uid of the newly selected device
    '''
    if uid == self._cur_uid:
      print 'Already Selected'
      return
    self._cur_uid = uid
    pid_key = 'DEVICE_LABEL'
    self.ola_thread.rdm_get(self.universe.get(), uid, 0, 'IDENTIFY_DEVICE', 
                  lambda b, s, uid = uid:self._get_identify_complete(uid, b, s))
    data = self._uid_dict[uid]
    flow = controlflow.RDMControlFlow(
        self.universe.get(), uid, [
            actions.GetSupportedParams(data, self.ola_thread.rdm_get),
            actions.GetDeviceInfo(data, self.ola_thread.rdm_get)
        ],
        self._device_changed_complete)
    flow.run()

  def _device_changed_complete(self):
    '''called once the control flow created in device_selected completes
    '''
    self._uid_dict[self._cur_uid]['PARAM_NAMES'] = set()
    for pid_key in self._uid_dict[self._cur_uid]['SUPPORTED_PARAMETERS']:
      pid = self._pid_store.GetPid(pid_key)
      if pid is not None:
        self._uid_dict[self._cur_uid]['PARAM_NAMES'].add(pid.name)
    print 'Device selected: %s' % self._uid_dict[self._cur_uid]
    self._notebook.update()

  def _get_identify_complete(self, uid, succeeded, value):
    ''' Callback for rdm_get in device_selected.

        Sets the checkbox's state to that of the currently selected device
    '''
    if succeeded: 
      self.id_state.set(value['identify_state'])

  def fetch_universes(self, callback):
    self.ola_thread.fetch_universes(self.fetch_universes_complete)

  def fetch_universes_complete(self, succeeded, universes):

    if succeeded:
      for universe in universes:
        self.universe_dict[universe.id] = UniverseObj(universe.id, universe.name)
        self.universe_menu.add_item(universe.name, 
          lambda i = universe.id: self._set_universe(i))
    else:
      print 'could not find active universe'

  def _set_universe(self, universe_id):
    ' sets the int var self.universe to the value of i '
    print universe_id
    self.universe.set(universe_id)
    self.device_menu.clear_menu()
    if not self.universe_dict[universe_id].discovery_run:
      self.discover()
    else:
      for uid in self.universe_dict[universe_id].uids:
        self._add_device_to_menu(uid)

  def discover(self):
    ' runs discovery for the current universe. '
    universe_id = self.universe.get()
    self.ola_thread.run_discovery(universe_id, 
            lambda status, uids:self._upon_discover(status, uids, universe_id))
    if self.auto_disc.get():
      self.ola_thread.add_event(5000, self.discover)
    else: 
      print 'Automatic discovery is off.'
  
  def _upon_discover(self, status, uids, universe_id):
    ' callback for client.runRDMDiscovery. '
    if self.universe.get() != universe_id:
      return
    self.universe_dict[universe_id].set_uids(uids)
    if not uids:
      self.device_menu.clear_menu()
    for uid in uids:
      if uid not in self._uid_dict.keys():
        self._uid_dict[uid] = {}
        self.ola_thread.rdm_get(self.universe.get(), uid, 0, 'DEVICE_LABEL', 
                             lambda b, s, uid = uid:self._add_device(uid, b, s),
                             [])

  def identify(self):
    ''' Command is called by id_box.

        sets the value of the device's identify field based on the value of 
        id_box.
    '''
    if self._cur_uid is None:
      return
    self.ola_thread.rdm_set(self.universe.get(), self._cur_uid, 0, 
              'IDENTIFY_DEVICE', 
              lambda b, s, uid = self._cur_uid
        :self._set_identify_complete(uid, b, s), 
              [self.id_state.get()])

  def _add_device(self, uid, error, data):
    ''' callback for the rdm_get in upon_discover.
        populates self.device_menu
    '''
    if error is None:
      self._uid_dict.setdefault(uid, {})['DEVICE_LABEL'] = data['label']
    else:
      self._uid_dict.setdefault(uid, {})['DEVICE_LABEL'] = ''
    self._add_device_to_menu(uid)

  def _set_identify_complete(self, uid, succeded, value):
    ''' callback for the rdm_set in identify. '''
    print 'identify %s' % value
    self._uid_dict[self._cur_uid] = value

  # ============================================================================
  # ============================ RDM Gets ======================================

  def get_basic_information(self):
    ''' creates and calls the action flow for retrieving information for the
        first tab of the notebook. 

        Triggered by: the control flow class, originally from the notebook
        initialization and "Device Information" tab selection.
    '''
    if self._cur_uid is None:
      print 'you need to select a device'
      return
    data = self._uid_dict[self._cur_uid]
    flow = controlflow.RDMControlFlow(
                  self.universe.get(), 
                  self._cur_uid, 
                  [
                  actions.GetProductDetailIds(data, self.ola_thread.rdm_get),
                  actions.GetDeviceModel(data, self.ola_thread.rdm_get),
                  actions.GetManufacturerLabel(data, self.ola_thread.rdm_get),
                  actions.GetFactoryDefaults(data, self.ola_thread.rdm_get),
                  actions.GetSoftwareVersion(data, self.ola_thread.rdm_get),
                  actions.GetBootSoftwareLabel(data, self.ola_thread.rdm_get),
                  actions.GetBootSoftwareVersion(data, self.ola_thread.rdm_get)
                  ],
                  self.update_basic_information)
    flow.run()

  def get_dmx_information(self):
    ''' creates and calls the action flow for retrieving information for the
        second tab of the notebook. 

        Triggered by: the control flow class, originally from the notebook
        initialization and "DMX512 Information" tab selection.
    '''

    if self._cur_uid is None:
      print 'you need to select a device.'
      return
    dmx_actions = []
    data = self._uid_dict[self._cur_uid]
    dmx_actions.append(actions.GetDmxPersonality(data, self.ola_thread.rdm_get))
    for i in xrange(data['DEVICE_INFO']['personality_count']):
      dmx_actions.append(actions.GetPersonalityDescription(
                                                  data, 
                                                  self.ola_thread.rdm_get, 
                                                  [i + 1]))
    dmx_actions.append(actions.GetStartAddress(data, self.ola_thread.rdm_get))
    dmx_actions.append(actions.GetSlotInfo(data, self.ola_thread.rdm_get))
    print 'dmx_footprint: %d' % data['DEVICE_INFO']['dmx_footprint']
    for i in xrange(data['DEVICE_INFO']['dmx_footprint']):
      dmx_actions.append(actions.GetSlotDescription(
                                                  data, 
                                                  self.ola_thread.rdm_get,
                                                  [i]))
    dmx_actions.append(
        actions.GetDefaultSlotValue(data, self.ola_thread.rdm_get))
    print i
    flow = controlflow.RDMControlFlow(
                self.universe.get(),
                self._cur_uid,
                dmx_actions,
                self.update_dmx_information)
    flow.run()

  def get_sensor_definitions(self):
    ''' gets the sensor definition for each sensor in the sensor count
    '''
    if self._cur_uid is None:
      return
    sensor_actions = []
    data = self._uid_dict[self._cur_uid]
    for i in xrange(data['DEVICE_INFO']['sensor_count']):
      sensor_actions.append(actions.GetSensorDefinition(data, 
                                                        self.ola_thread.rdm_get,
                                                        [i]))
                        
    flow = controlflow.RDMControlFlow(
                  self.universe.get(),
                  self._cur_uid,
                  sensor_actions,
                  self.update_sensor_information)
    flow.run()

  def get_sensor_value(self, sensor_number):
    """ gets the sensor value for the currently selected sensor

      Args: sensor_number: the number associated with the currently selected 
            sensor. 

      call originates in render_sensor_information in the notebook class.
    """
    if self._cur_uid is None:
      return
    sensor_actions = []
    data = self._uid_dict[self._cur_uid]
    sensor_actions = [actions.GetSensorValue(data,
                                             self.ola_thread.rdm_get,
                                             [sensor_number])]
                        
    flow = controlflow.RDMControlFlow(
                  self.universe.get(),
                  self._cur_uid,
                  sensor_actions,
                  lambda: self.display_sensor_data(sensor_number))
    flow.run()

  def get_setting_information(self):
    ''' creates and calls the action flow for retrieving information for the
        forth tab of the notebook. 

        Triggered by: the control flow class, originally from the notebook
        initialization and "Power and Lamp Settings" tab selection.
    '''
    if self._cur_uid is None:
      print 'you need to select a device'
      return
    data = self._uid_dict[self._cur_uid]
    flow = controlflow.RDMControlFlow(
                  self.universe.get(), 
                  self._cur_uid, 
                  [
                  actions.GetDeviceHours(data, self.ola_thread.rdm_get),
                  actions.GetLampHours(data, self.ola_thread.rdm_get),
                  actions.GetLampState(data, self.ola_thread.rdm_get),
                  actions.GetLampStrikes(data, self.ola_thread.rdm_get),
                  actions.GetLampOnMode(data, self.ola_thread.rdm_get),
                  actions.GetPowerCycles(data, self.ola_thread.rdm_get),
                  actions.GetPowerState(data, self.ola_thread.rdm_get),
                  ],
                  self.update_setting_information)
    flow.run()

  def get_config_information(self):
    ''' creates and calls the action flow for retrieving information for the
        fifth tab of the notebook. 

        Triggered by: the control flow class, originally from the notebook
        initialization and "Configure" tab selection.
    '''
    if self._cur_uid is None:
      print 'you need to select a device'
      return
    data = self._uid_dict[self._cur_uid]
    flow = controlflow.RDMControlFlow(
                  self.universe.get(), 
                  self._cur_uid, 
                  [
                  actions.GetLanguageCapabilities(data, self.ola_thread.rdm_get),
                  actions.GetLanguage(data, self.ola_thread.rdm_get),
                  actions.GetDisplayInvert(data, self.ola_thread.rdm_get),
                  actions.GetDisplayLevel(data, self.ola_thread.rdm_get),
                  actions.GetPanInvert(data, self.ola_thread.rdm_get),
                  actions.GetTiltInvert(data, self.ola_thread.rdm_get),
                  actions.GetPanTiltSwap(data, self.ola_thread.rdm_get),
                  actions.GetRealTimeClock(data, self.ola_thread.rdm_get)
                  ],
                  self.update_config_information)
    flow.run()
  
  # ============================ Notebook Updates ==============================
  # The following methods call into the notebook class and popluate the 
  # associted tab with RDM information

  def update_basic_information(self):
    # print "uid_dict: %s" % self._uid_dict[self._cur_uid]
    self._notebook.render_basic_information(self._uid_dict[self._cur_uid])

  def update_dmx_information(self):
    self._notebook.render_dmx_information(self._uid_dict[self._cur_uid])

  def update_setting_information(self):
    self._notebook.render_setting_information(self._uid_dict[self._cur_uid])

  def update_config_information(self):
    self._notebook.render_config_information(self._uid_dict[self._cur_uid])

  # the sensor tab is slightly different that those above. The first method
  # populates (update_sensor_information) the RDM menu on the sensor tab and the
  # second method displays the values being recorded/sensed by the sensor device 
  def update_sensor_information(self):
    self._notebook.render_sensor_information(self._uid_dict[self._cur_uid])

  def display_sensor_data(self,sensor_number):
    self._notebook.display_sensor_data(
        self._uid_dict[self._cur_uid],sensor_number)

  # ============================ RDM Sets ======================================
  def set_start_address(self, start_address):
    ''' Sets the start address of the current device.

        Args:
          start_address: the DMX address that is set as the start address.
    '''
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._set_address_complete(start_address, b, s)
    self.ola_thread.rdm_set(
        self.universe.get(), uid, 0, 'DMX_START_ADDRESS', callback, 
        [start_address])

  def _set_address_complete(self, start_address, error, data):
    ''' callback method from the ola call triggered in the above method

        Args:
          start_address: the new DMX address of the current device
          error: None, if the ola thread call succeeded, the error returned if
            the call fails
          data: 
    '''
    print 'set start address callback'
    if error is None:
      pid_dict = self._uid_dict[self._cur_uid]
      pid_dict['DEVICE_INFO']['dmx_start_address'] = start_address
      pid_dict['DMX_START_ADDRESS'] = start_address
      print 'DMX start address set to %s' % start_address
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_dmx_personality(self, personality):
    ''' sets the DMX personality of the current RDM device

        Args:
          personality: the personality that the device will be set to if the 
          ola call succeeds
    '''
    if self._cur_uid is None:
      return
    data = self._uid_dict[self._cur_uid]
    flow_actions = [actions.SetDMXPersonality(data, self.ola_thread.rdm_set,
                                              [personality])]
    flow = controlflow.RDMControlFlow(
                self.universe.get(),
                self._cur_uid,
                flow_actions,
                lambda b, s: self._get_slot_info(personality, b, s))
    flow.run()

  def _get_slot_info(self, personality, error, data):
    '''
        Args:
          personality: the personality of the current device
          error: the error returned if the previous ola call fails, otherwise
          this will be None
          data: 16 bit slot number, data to be passed to the ola thread
    '''
    print 'getting slot info...'
    if error is None:
      data = self._uid_dict[self._cur_uid]
      flow_actions = []
      for slot in xrange(self._uid_dict[self._cur_uid]
          ['DMX_PERSONALITY_DESCRIPTION']
          [personality]['slots_required']):
        flow_actions.append(actions.GetSlotDescription(
            data, self.ola_thread.rdm_get, [slot]))
        flow_actions.append(actions.GetSlotInfo(data, self.ola_thread.rdm_get))
        flow_actions.append(actions.GetDefaultSlotValue(
            data, self.ola_thread.rdm_get))
      flow = controlflow.RDMControlFlow(
                self.universe.get(),
                self._cur_uid,
                flow_actions,
                lambda b, s: self._set_dmx_personality_complete(b, s))
      flow.run()
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def _set_dmx_personality_complete(self, error, data):
    ''' the final call back from the set DMX personality control flow

        Args:
          error: None, or the error returned by the ola call
          data: Not Present
    '''
    if error is None:
      self._notebook.set_dmx_personality_complete(self._uid_dict[self._cur_uid])
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)

  def set_display_level(self, level):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._display_level_complete(uid, level, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'DISPLAY_LEVEL',
                              callback,
                              [level])

  def _display_level_complete(self, uid, level, error, data):
    if error is None:
      self._uid_dict[uid]['DISPLAY_LEVEL'] = level
      self._notebook.set_display_level_complete(level)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_lamp_state(self, state):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._set_lamp_state_complete(uid, state, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'LAMP_STATE',
                              callback,
                              [state])

  def _set_lamp_state_complete(self, uid, state, error, data):
    if error is None:
      self._uid_dict[uid]['LAMP_STATE'] = state
      self._notebook.set_lamp_state_complete(state)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_lamp_on_mode(self, mode):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._set_lamp_on_mode_complete(uid, mode, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'LAMP_ON_MODE',
                              callback,
                              [mode])
    
  def _set_lamp_on_mode_complete(self, uid, mode, error, data):
    if error is None:
      self._uid_dict[uid]['LAMP_ON_MODE'] = mode
      self._notebook.set_lamp_on_mode_complete(mode)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_power_state(self, state):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._set_power_state_complete(uid, state, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'POWER_STATE',
                              callback,
                              [state])
    
  def _set_power_state_complete(self, uid, state, error, data):
    if error is None:
      self._uid_dict[uid]['POWER_STATE'] = state
      self._notebook.set_power_state_complete(state)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_language(self, language):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._language_complete(uid, language, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'LANGUAGE',
                              callback,
                              [language])

  def _language_complete(self, uid, language, error, data):
    if error is None:
      self._uid_dict[uid]['LANGUAGE'] = language
      self._notebook.set_language_complete(language)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_display_invert(self, invert):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._display_invert_complete(uid, invert, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'DISPLAY_INVERT',
                              callback,
                              [invert])

  def _display_invert_complete(self, uid, invert, error, data):
    if error is None:
      self._uid_dict[uid]['DISPLAY_INVERT'] = invert
      self._notebook.set_display_invert_complete(invert)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_pan_invert(self, invert):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._pan_invert_complete(uid, invert, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'PAN_INVERT',
                              callback,
                              [invert])

  def _pan_invert_complete(self, uid, invert, error, data):
    if error is None:
      self._uid_dict[uid]['PAN_INVERT'] = invert
      self._notebook.set_pan_invert_complete(invert)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_tilt_invert(self, invert):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._tilt_invert_complete(uid, invert, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                              uid,
                              0,
                              'TILT_INVERT',
                              callback,
                              [invert])

  def _tilt_invert_complete(self, uid, invert, error, data):
    if error is None:
      self._uid_dict[uid]['TILT_INVERT'] = invert
      self._notebook.set_tilt_invertComplete(invert)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def set_pan_tilt_swap(self, swap):
    if self._cur_uid is None:
      return
    uid = self._cur_uid
    callback = lambda b, s: self._pan_tilt_swap_complete(uid, swap, b, s)
    self.ola_thread.rdm_set(self.universe.get(),
                            uid,
                            0,
                            'PAN_TILT_SWAP',
                            callback,
                            [swap])

  def _pan_tilt_swap_complete(self, uid, swap, error, data):
    if error is None:
      self._uid_dict[uid]['PAN_TILT_SWAP'] = swap
      self._notebook.set_pan_tilt_swap_complete(swap)
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def record_sensor(self, sensor_number):
    self.ola_thread.rdm_set(self.universe.get(),
                            self._cur_uid,
                            0,
                            'RECORD_SENSORS',
                            lambda b, s: self.record_sensor_complete(b, s),
                            [sensor_number])
  
  def record_sensor_complete(self, error, data):
    if error is None:
      pass
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  def clear_sensor(self, sensor_number):
    sensor_actions = []
    data = self._uid_dict[self._cur_uid]
    sensor_actions.append(actions.SetSensorValue(
        data, self.ola_thread.rdm_set, [sensor_number]))
    sensor_actions.append(actions.GetSensorValue(
        data, self.ola_thread.rdm_get, [sensor_number]))
    sensor_actions.append(actions.GetSensorDefinition(
        data, self.ola_thread.rdm_get, [sensor_number]))
    flow = controlflow.RDMControlFlow(
                  self.universe.get(),
                  self._cur_uid,
                  sensor_actions,
                  lambda: self.display_sensor_data(sensor_number))
    flow.run()

  def clear_sensor_complete(self, error, data):
    if error is None:
      pass
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()

  # ================================ Callbacks =================================


  def set_device_label(self, label):
    uid = self._cur_uid
    callback = (lambda b, s: self.set_device_label_complete(uid, label, b, s))
    self.ola_thread.rdm_set(self.universe.get(), 
                              uid,
                              0, 
                              'DEVICE_LABEL',
                              callback,
                              [label]
                              )

  def set_device_label_complete(self, uid, label, error, data):
    if error is None:
      index = self._uid_dict[self._cur_uid]['index']
      self._uid_dict[self._cur_uid]['DEVICE_LABEL'] = label
      self.device_menu.entryconfigure(index, label = '%s (%s)'%(
                  self._uid_dict[uid]['DEVICE_LABEL'], uid))
    else:
      d = RDMDialog(self.root, error)
      self.root.wait_window(d.top)
      self._notebook.update()
    # store the results in the uid dict
    self.root.update_idletasks()
    self._notebook.update()

  def _add_device_to_menu(self, uid):
    label = self._uid_dict[uid]['DEVICE_LABEL']
    if label == '':
      menu_label = '%s' % uid
    else:
      menu_label = '%s (%s)' % (label, uid)
    index = self.device_menu.add_item(menu_label, lambda:self.device_selected(uid))
    self._uid_dict[uid]['index'] = index

  def main(self):
    print 'Entering main loop'
    self.root.mainloop()


if __name__  ==  '__main__':
  logging.basicConfig(level=logging.INFO, format='%(message)s')
  display = DisplayApp(800, 600)
  display.main()
