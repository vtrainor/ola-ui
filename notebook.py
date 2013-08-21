import Tkinter as tk
import simple_ui
import ttk
import ola.RDMConstants as RDMConstants
from rdm_menu import RDMMenu
import PIDDict

class RDMNotebook(object):
  def __init__(self, root, controller, width=800, height=500, side=tk.TOP):
    """ Builds the ttk.Notebook """
    self.root = root
    self._controller = controller
    self.init_dx = width
    self.init_dy = height
    self.side = side
    self.objects = {}
    self.pid_location_dict = {}
    self._notebook = ttk.Notebook(self.root, name="nb", height=height,
                                  width=width)
    self._notebook.bind('<<NotebookTabChanged>>', self._tab_changed)
    self.populate_defaults()

  def populate_defaults(self):
    """ creates the default frames. """
    self.info_tab = self._create_tab("info_tab", "Device Information")
    self._init_info()
    self.dmx_tab = self._create_tab("dmx_tab", "DMX512 Setup")
    self._init_dmx()
    self.sensor_tab = self._create_tab("sensor_tab", "Sensors")
    self._init_sensor()
    self.setting_tab = self._create_tab("setting_tab", 
                                        "Power and Lamp Settings")
    self._init_setting()
    self.config_tab = self._create_tab("config_tab", "Configuration")
    self._init_config()
    tabs = ["PRODUCT_INFO", "DMX512_SETUP", "SENSORS",
            "POWER_LAMP_SETTINGS", "CONFIGURATION"]
    for tab in tabs:
      self._grid_info(self.objects[tab])
    self._notebook.pack(side = self.side)

  def activate(self):
    pass
# ==============================================================================
# ============================ Tab Inits =======================================
# ==============================================================================

  def _init_info(self):
    """
    """
    # Text Variables:
    self.protocol_version = tk.StringVar(self.info_tab)
    self.device_model = tk.StringVar(self.info_tab)
    self.product_category = tk.StringVar(self.info_tab)
    self.software_version = tk.StringVar(self.info_tab)
    self.sub_device_count = tk.StringVar(self.info_tab)
    self.product_detail_ids = tk.StringVar(self.info_tab)
    self.manufacturer_label = tk.StringVar(self.info_tab)
    self.device_label = tk.StringVar(self.info_tab)
    self.boot_software = tk.StringVar(self.info_tab)
    # Widgets:
    #device label entry boc value should be capped at 32
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.factory_defaults_button = tk.Checkbutton(
        self.info_tab, variable = self.factory_defaults)
    self.device_label_button = tk.Button(self.info_tab, 
                                         text = "Update Device Label",
                                         command = self.device_label_set)
    self.objects["PRODUCT_INFO"] = [
        tk.Label(self.info_tab, text = "RDM Protocol Version"),
        tk.Label(self.info_tab, textvariable = self.protocol_version),
        tk.Label(self.info_tab, text = "Device Model"),
        tk.Label(self.info_tab, textvariable = self.device_model),
        tk.Label(self.info_tab, text = "Product Category:"),
        tk.Label(self.info_tab, textvariable = self.product_category),
        tk.Label(self.info_tab, text = "Software Version:"),
        tk.Label(self.info_tab, textvariable = self.software_version),
        tk.Label(self.info_tab, text = "Product Details:"),
        tk.Label(self.info_tab, textvariable = self.product_detail_ids),
        tk.Label(self.info_tab, text = "Sub-Device Count"),
        tk.Label(self.info_tab, textvariable = self.sub_device_count),
        tk.Label(self.info_tab, text = "Manufacturer:"),
        tk.Label(self.info_tab, textvariable = self.manufacturer_label),
        tk.Label(self.info_tab, text = "Device Label:"),
        tk.Entry(self.info_tab, textvariable = self.device_label),
        tk.Label(self.info_tab, text = "Factory Defaults:"),
        tk.Checkbutton(self.info_tab, variable = self.factory_defaults),
        tk.Label(self.info_tab, text = "Boot Software Version:"),
        tk.Label(self.info_tab, textvariable = self.boot_software),
        self.device_label_button,
        tk.Label(self.info_tab, text = ""),
    ]

  def _init_dmx(self):
    """
    """
    # Text Variables
    self.dmx_footprint = tk.StringVar(self.dmx_tab)
    self.dmx_start_address = tk.StringVar(self.dmx_tab)
    self.slot_required = tk.StringVar(self.dmx_tab)
    self.personality_name = tk.StringVar(self.dmx_tab)
    self.slot_number = tk.StringVar(self.dmx_tab)
    self.slot_name = tk.StringVar(self.dmx_tab)
    self.slot_type = tk.StringVar(self.dmx_tab)
    self.slot_label_id = tk.StringVar(self.dmx_tab)
    self.default_slot_value = tk.StringVar(self.dmx_tab)
    # Widgets
    self.start_address_entry = tk.Entry(
        self.dmx_tab, textvariable = self.dmx_start_address)
    # validatecommand make sure between 1 and 512
    self.dmx_personality_menu = RDMMenu(
        self.dmx_tab, "Personality description not supported.", "")
    self.slot_menu = RDMMenu(
        self.dmx_tab, "No slot description.", "Choose Slot")

    self.objects["DMX512_SETUP"] = [
        tk.Label(self.dmx_tab, text = "DMX Footprint:"),
        tk.Label(self.dmx_tab, textvariable = self.dmx_footprint),
        tk.Label(self.dmx_tab, text = "DMX Start Address:"),
        self.start_address_entry,
        tk.Button(self.dmx_tab, text = 'Set Start Address', 
                  command = self.set_start_address),
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, text = "Current Personality:"),
        self.dmx_personality_menu,
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.slot_required),
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.personality_name),
        tk.Label(self.dmx_tab, text = "Slot Info:"),
        self.slot_menu,
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.slot_name),
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.slot_type),
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.slot_label_id),
        tk.Label(self.dmx_tab, text = ""),
        tk.Label(self.dmx_tab, textvariable = self.default_slot_value),
    ]

  def _init_sensor(self):
    """
    """
    # Text Variable
    self.sensor_type = tk.StringVar(self.sensor_tab)
    self.sensor_unit = tk.StringVar(self.sensor_tab)
    self.sensor_prefix = tk.StringVar(self.sensor_tab)
    self.sensor_range = tk.StringVar(self.sensor_tab)
    self.normal_range = tk.StringVar(self.sensor_tab)
    self.supports_recording = tk.StringVar(self.sensor_tab)
    self.supports_lowest_highest = tk.StringVar(self.sensor_tab)
    self.sensor_name = tk.StringVar(self.sensor_tab)
    self.sensor_number = tk.StringVar(self.sensor_tab)
    self.present_value = tk.StringVar(self.sensor_tab)
    self.lowest = tk.StringVar(self.sensor_tab)
    self.highest = tk.StringVar(self.sensor_tab)
    self.recorded = tk.StringVar(self.sensor_tab)
    # Widgets
    self.sensor_menu = RDMMenu(
        self.sensor_tab, "Sensor information not provided.", "Choose Sensor")
    self.record_sensor_button = tk.Button(
        self.sensor_tab, text="Record Sensor", state=tk.DISABLED)
    self.clear_sensor_button = tk.Button(
        self.sensor_tab, text='Clear Sensor', state=tk.DISABLED)
    self.refresh_sensor_button = tk.Button(
        self.sensor_tab, text = 'Refresh', state=tk.DISABLED)

    self.objects["SENSORS"] = [
        tk.Label(self.sensor_tab, text = "Choose Sensor"),
        self.sensor_menu,
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.sensor_type),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.sensor_unit),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.sensor_prefix),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.sensor_range),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.normal_range),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.supports_recording),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.supports_lowest_highest),                              
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.present_value),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.lowest),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.highest),
        tk.Label(self.sensor_tab, text = ""),
        tk.Label(self.sensor_tab, textvariable = self.recorded),
        tk.Label(self.sensor_tab, text = ""),
        self.record_sensor_button,
        tk.Label(self.sensor_tab, text = ""),
        self.clear_sensor_button,
        tk.Label(self.sensor_tab, text = ""),
        self.refresh_sensor_button
    ]

  def _init_setting(self):
    """
    """
    # sText Varibles
    self.device_hours = tk.StringVar(self.setting_tab)
    self.lamp_hours = tk.StringVar(self.setting_tab)
    self.lamp_strikes = tk.StringVar(self.setting_tab)
    self.lamp_state = tk.StringVar(self.setting_tab)
    self.lamp_on_mode = tk.StringVar(self.setting_tab)
    self.device_power_cycles = tk.StringVar(self.setting_tab)
    self.power_state = tk.StringVar(self.setting_tab)
    # Widgets
    self.lamp_state_menu = RDMMenu(self.setting_tab,
                                   'Lamp state not supported.',
                                   '')
    self.lamp_on_mode_menu = RDMMenu(self.setting_tab,
                                     'Lamp on mode not supported',
                                     '')
    self.power_state_menu = RDMMenu(self.setting_tab,
                                    'Power state not supported.',
                                    '')

    self.objects["POWER_LAMP_SETTINGS"] = [
        tk.Label(self.setting_tab, text = "Device Hours:"),
        tk.Label(self.setting_tab, textvariable = self.device_hours),
        tk.Label(self.setting_tab, text = "Device Power Cycles:"),
        tk.Label(self.setting_tab, textvariable = self.device_power_cycles),
        tk.Label(self.setting_tab, text = "Lamp Hours:"),
        tk.Label(self.setting_tab, textvariable = self.lamp_hours),
        tk.Label(self.setting_tab, text = "Lamp Strikes:"),
        tk.Label(self.setting_tab, textvariable = self.lamp_strikes),
        tk.Label(self.setting_tab, text = "Lamp State:"),
        self.lamp_state_menu,
        tk.Label(self.setting_tab, text = "Lamp On Mode:"),
        self.lamp_on_mode_menu,
        tk.Label(self.setting_tab, text = "Power State:"),
        self.power_state_menu
    ]

  def _init_config(self):
    """
    """
    # Variables
    self.display_invert = tk.StringVar(self.config_tab)
    self.display_level = tk.IntVar(self.config_tab)
    self.pan_invert = tk.BooleanVar(self.config_tab)
    self.tilt_invert = tk.BooleanVar(self.config_tab)
    self.pan_tilt_swap = tk.BooleanVar(self.config_tab)
    self.real_time_clock = tk.StringVar(self.config_tab)
    # Widgets
    self.language_menu = RDMMenu(
        self.config_tab, "Languages not supported.", "")
    self.display_invert_menu = tk.OptionMenu(self.config_tab,
                                            self.display_invert, 
                                            *PIDDict.DISPLAY_INVERT.values(),
                                            command = self._set_display_invert)
    self.display_level_menu = tk.Scale(
        self.config_tab, 
        from_ = 0, 
        to = 255, 
        variable=self.display_level,
        orient=tk.HORIZONTAL, 
        command = self._controller.set_display_level,
        length = 255, 
        state = tk.DISABLED, 
        tickinterval = 255)
    self.pan_invert_button = tk.Checkbutton(self.config_tab,
                                            variable = self.pan_invert,
                                            command = self._set_pan_invert,
                                            state = tk.DISABLED)
    self.tilt_invert_button = tk.Checkbutton(self.config_tab,
                                             variable = self.tilt_invert,
                                             command = self._set_tilt_invert,
                                             state = tk.DISABLED)
    self.pan_tilt_swap_button = tk.Checkbutton(
      self.config_tab,
        variable = self.pan_tilt_swap,
        command = self._set_pan_tilt_swap,
        state = tk.DISABLED)
    self.objects["CONFIGURATION"] = [
        tk.Label(self.config_tab, text = "Device Language:"),
        self.language_menu,
        tk.Label(self.config_tab, text = "Display Invert:"),
        self.display_invert_menu,
        tk.Label(self.config_tab, text = "Display Level:"),
        self.display_level_menu,
        tk.Label(self.config_tab, text = "Pan Invert:"),
        self.pan_invert_button,
        tk.Label(self.config_tab, text = "Tilt Invert:"),
        self.tilt_invert_button,
        tk.Label(self.config_tab, text = "Pan Tilt Swap"),
        self.pan_tilt_swap_button,
        tk.Label(self.config_tab, text = "Real Time Clock"),
        tk.Label(self.config_tab, textvariable = self.real_time_clock) 
    ]


  # ============================================================================
  # ============================== Update Tabs =================================
  # ============================================================================

  def update(self):
    index = self._notebook.index('current')
    print 'The selected tab changed to %d' % index
    if index == 0:
      self._controller.get_basic_information()
    elif index == 1:
      self._controller.get_dmx_information()
    elif index == 2:
      self._controller.get_sensor_definitions()
    elif index == 3:
      self._controller.get_setting_information()
    elif index == 4:
      self._controller.get_config_information()

  # ========================= Information Rendering ============================

  def render_basic_information(self, param_dict):
    '''
    Uses the data in param_dict to display the DMX information for the device
    Called when the tab is selected, or the device changed.
    Ultimate callback function for control flow, 'get_basic_information'.

    Args:
      param_dict: dictionary of pids for the current uid. In the form:
                                                                    {PID: data}

          NOTE: data may be in the form of a int, string or dict and is treated
              differently in each case.
    '''
    device_info = param_dict["DEVICE_INFO"]
    self.protocol_version.set(
        "Version %d.%d" % (
        device_info["protocol_major"], 
        device_info["protocol_minor"]))
    self.device_model.set(param_dict["DEVICE_INFO"]["device_model"])
    self.device_model.set("%s (%d)" % (
                          param_dict.get("DEVICE_MODEL_DESCRIPTION", 'N/A'),
                          device_info["device_model"]))
    index = device_info["product_category"]
    self.product_category.set(RDMConstants.PRODUCT_CATEGORY_TO_NAME.get(index, 
        "").replace("_"," "))
    self.sub_device_count.set(param_dict["DEVICE_INFO"]["sub_device_count"])

    self.software_version.set("%s (%d)" % (
                              param_dict.get("SOFTWARE_VERSION_LABEL", "N/A"),
                              device_info["software_version"]))
    self.sub_device_count.set(device_info["sub_device_count"])
    if "PRODUCT_DETAIL_ID_LIST" in param_dict:
      ids = param_dict["PRODUCT_DETAIL_ID_LIST"]
      names = ', '.join(RDMConstants.PRODUCT_DETAIL_IDS_TO_NAME[id]
                        for id in ids).replace("_", " ")
      self.product_detail_ids.set(names)
    self.manufacturer_label.set(param_dict.get("MANUFACTURER_LABEL", "N/A"))
    self.device_label.set(param_dict.get("DEVICE_LABEL", "N/A"))
    self.factory_defaults.set(param_dict.get("FACTORY_DEFAULTS", "N/A"))
    boot_software = 'N/A'
    boot_software_version = param_dict.get('BOOT_SOFTWARE_VERSION')
    boot_software_label = param_dict.get('BOOT_SOFTWARE_LABEL')
    if boot_software_version and boot_software_label:
      boot_software = '%s (%d)' % (boot_software_label, boot_software_version)
    elif boot_software_label:
      boot_software =  boot_software_label
    elif boot_software_version:
      boot_software =  boot_software_version
    self.boot_software.set(boot_software)

  def render_dmx_information(self, param_dict):
    '''
    Uses the data in param_dict to display the DMX information for the device
    Called when the tab is selected, or the device changed.
    Ultimate callback function for control flow, 'get_dmx_information'.

    Args:
      param_dict: dictionary of pids for the current uid. In the form:
                                                                    {PID: data}

          NOTE: data may be in the form of a int, string or dict and is treated
              differently in each case.
    '''
    print "param_dict: %s" % param_dict
    device_info = param_dict["DEVICE_INFO"]
    self.dmx_personality_menu.clear_menu()
    self.slot_menu.clear_menu()
    self._display_personality_decription('N/A', 'N/A')
    if "DMX_PERSONALITY_DESCRIPTION" in param_dict:
      personalities = param_dict["DMX_PERSONALITY_DESCRIPTION"]
      for personality in personalities.iteritems():
        print personality
        self.dmx_personality_menu.add_item(
            self._get_personality_string(personality[1]),
            lambda i = personality[0]:self._controller.set_dmx_personality(i))
      personality_id = device_info['current_personality']
      self.dmx_personality_menu.set(self._get_personality_string(
          personalities[personality_id]))
      s = personalities[personality_id]['slots_required']
      p = personality_id
      self._display_personality_decription(s, p)
    self.dmx_footprint.set(param_dict["DEVICE_INFO"]["dmx_footprint"])
    start_address = param_dict["DEVICE_INFO"]["dmx_start_address"]
    if start_address == 0xffff:
      self.dmx_start_address.set('N/A')
      self.start_address_entry.config(state = tk.DISABLED)
    else:
      self.dmx_start_address.set(start_address)
      self.start_address_entry.config(state = tk.NORMAL)
    if "SLOT_INFO" in param_dict:
      for index in xrange(param_dict["DEVICE_INFO"]["dmx_footprint"]):
        self.slot_menu.add_item(
            "Slot Number %d" % index,
            lambda i = index:self._display_slot_info(i, param_dict))

  def render_sensor_information(self, param_dict):
    '''
    Uses the data in param_dict to display the DMX information for the device
    Called when the tab is selected, or the device changed.
    Ultimate callback function for control flow, 'get_sensor_information'.

    Args:
      param_dict: dictionary of pids for the current uid. In the form:
                                                                    {PID: data}

          NOTE: data may be in the form of a int, string or dict and is treated
              differently in each case.
    '''
    self.sensor_type.set('')
    self.sensor_unit.set('')
    self.sensor_prefix.set('')
    self.sensor_range.set('')
    self.normal_range.set('')
    self.supports_recording.set('')
    self.present_value.set('')
    self.lowest.set('')
    self.highest.set('')
    self.recorded.set('')
    sensor_info = {}
    self.sensor_menu.clear_menu()
    for index, sensor in param_dict.get('SENSOR_DEFINITION', {}).iteritems():
      self.sensor_menu.add_item('%s' % sensor['name'],
                                lambda i=index: self._populate_sensor_tab(i))
   

  def render_setting_information(self, param_dict):
    '''
    Uses the data in param_dict to display the DMX information for the device
    Called when the tab is selected, or the device changed.
    Ultimate callback function for control flow, 'GetSettingsInformation'.

    Args:
      param_dict: dictionary of pids for the current uid. In the form:
                                                                    {PID: data}

          NOTE: data may be in the form of a int, string or dict and is treated
              differently in each case.
    '''
    print "PARAM_DICT: %s" % param_dict
    self.device_hours.set(param_dict.get('DEVICE_HOURS', 'N/A'))
    self.lamp_hours.set(param_dict.get('LAMP_HOURS', 'N/A'))
    self.device_power_cycles.set(param_dict.get("DEVICE_POWER_CYCLES", "N/A"))
    self.lamp_strikes.set(param_dict.get('LAMP_STRIKES', 'N/A'))
    self.lamp_state_menu.config(state = tk.DISABLED)
    self.lamp_on_mode_menu.config(state = tk.DISABLED)
    self.power_state_menu.config(state = tk.DISABLED)

    if 'LAMP_STATE' in param_dict:
      self.lamp_state_menu.config(state = tk.NORMAL)
      for key, value in PIDDict.LAMP_STATE.iteritems():
        self.lamp_state_menu.add_item(
            value, lambda k=key: self._controller.set_lamp_state(k))
      self.lamp_state_menu.set(PIDDict.LAMP_STATE[param_dict['LAMP_STATE']])

    if 'LAMP_ON_MODE' in param_dict:
      self.lamp_on_mode_menu.config(state = tk.NORMAL)
      for key, value in PIDDict.LAMP_ON_MODE.iteritems():
        self.lamp_on_mode_menu.add_item(value, 
                                        lambda k=key: self._set_lamp_on_mode(k))
      self.lamp_on_mode_menu.set(
          PIDDict.LAMP_ON_MODE[param_dict['LAMP_ON_MODE']])

    if 'POWER_STATE' in param_dict:
      self.power_state_menu.config(state = tk.NORMAL)
      for key, value in PIDDict.POWER_STATE.iteritems():
        self.power_state_menu.add_item(value, 
                                       lambda k=key: self._set_power_state(k))
      self.power_state_menu.set(PIDDict.POWER_STATE[param_dict['POWER_STATE']])

  def render_config_information(self, param_dict):
    '''
    Uses the data in param_dict to display the DMX information for the device
    Called when the tab is selected, or the device changed.
    Ultimate callback function for control flow, 'get_config_information'.

    Args:
      param_dict: dictionary of pids for the current uid. In the form:
                                                                    {PID: data}

          NOTE: data may be in the form of a int, string or dict and is treated
              differently in each case.
    '''
    self.language_menu.clear_menu()
    if 'LANGUAGE_CAPABILITIES' in param_dict:
      self.language_menu.config(state = tk.NORMAL)
      for value in param_dict['LANGUAGE_CAPABILITIES']:
        language = value['language']
        self.language_menu.add_item(language, 
                                    lambda l = language: self._set_language(l))
    self.language_menu.set(param_dict.get('LANGUAGE', 'N/A'))

    if "DISPLAY_LEVEL" in param_dict:
      self.display_level.set(param_dict['DISPLAY_LEVEL'])
      self.display_level_menu.config(state = tk.NORMAL)
    else:
      self.display_level.set(0)
      self.display_level_menu.config(state = tk.DISABLED)

    if 'DISPLAY_INVERT' in param_dict:
      display_invert = PIDDict.DISPLAY_INVERT [param_dict['DISPLAY_INVERT']]
      self.display_invert.set(display_invert)
      self.display_invert_menu.config(state = tk.NORMAL)
    else:
      self.display_invert.set('N/A')
      self.display_invert_menu.config(state = tk.DISABLED)

    if 'PAN_INVERT' in param_dict:
      self.pan_invert.set(param_dict['PAN_INVERT'])
      self.pan_invert_button.config(state = tk.NORMAL)
    else:
      self.pan_invert.set(False)
      self.pan_invert_button.config(state = tk.DISABLED)

    if 'TILT_INVERT' in param_dict:
      self.tilt_invert.set(param_dict['TILT_INVERT'])
      self.tilt_invert_button.config(state = tk.NORMAL)
    else:
      self.tilt_invert.set(False)
      self.tilt_invert_button.config(state = tk.DISABLED)

    if 'PAN_TILT_SWAP' in param_dict:
      self.pan_tilt_swap.set(param_dict['PAN_TILT_SWAP'])
      self.pan_tilt_swap_button.config(state = tk.NORMAL)
    else:
      self.pan_tilt_swap.set(False)
      self.pan_tilt_swap_button.config(state = tk.DISABLED)

    if 'REAL_TIME_CLOCK' in param_dict:
      clock = param_dict['REAL_TIME_CLOCK']
      self.real_time_clock.set("%d:%d:%d %d/%d/%d" % (clock['hour'],
                                                      clock['minute'],
                                                      clock['second'],
                                                      clock['day'],
                                                      clock['month'],
                                                      clock['year']
                                                      ))

  # ============================================================================
  # ============================ RDM Set Methods ===============================
  # ============================================================================
  def device_label_set(self):
    """
    """
    self._controller.SetDeviceLabel(self.device_label.get())

  def set_start_address(self):
    '''
    start of control flow for setting the dmx_start_address of a device.
    '''
    start_address = self.dmx_start_address.get()
    self._controller.set_start_address(start_address)

  # def _set_lamp_state(self, state):
  #   '''
  #   Internal Function, first function in the 'SetLampState' control flow.

  #   Args:
  #     state: int, see PIDDict.LAMP_STATE for state name.
  #   '''
  #   self._controller.set_lamp_state(state)

  def set_lamp_state_complete(self, state):
    '''
    Ultimate callback for, 'SetLampState' control flow.

    Args:
      state: int, see PIDDict.LAMP_STATE for state name.
    '''
    if self.lamp_state_menu.get() != PIDDict.LAMP_STATE[state]:
      self.lamp_state_menu.set(PIDDict.LAMP_STATE[state])

  def _set_lamp_on_mode(self, mode):
    '''
    Infternal Function, first function in the 'SetLampOnMode' control flow.

    Args:
      mode: int, see PIDDict.LAMP_ON_MODE for mode names.
    '''
    self._controller.set_lamp_on_mode(mode)

  def set_lamp_on_mode_complete(self, mode):
    '''
    Ulitmate callback for 'SetLampOnMode' control flow

    Args:
      mode: int, see PIDDict.LAMP_ON_MODE for mode names.
    '''
    if self.lamp_on_mode_menu.get() != PIDDict.LAMP_ON_MODE[mode]:
      self.lamp_on_mode_menu.set(PIDDict.LAMP_ON_MODE[mode])

  def _set_power_state(self, state):
    '''
    Infternal Function, first function in the 'SetPowerState' control flow.

    Args:
      state: int, see PIDDict.LAMP_STATE for state name.
    '''
    self._controller.set_power_state(state)

  def set_power_state_complete(self, state):
    '''

    '''
    if self.power_state_menu.get() != PIDDict.POWER_STATE[state]:
      self.power_state_menu.set(PIDDict.POWER_STATE[state])

  def set_dmx_personality_complete(self, param_dict):
    print param_dict
    personality = param_dict['DEVICE_INFO']['current_personality']
    slots_required = param_dict.get("DMX_PERSONALITY_DESCRIPTION", 
                                    {})[personality].get(
                                    "slots_required", 
                                    "N/A")
    self._display_personality_decription(slots_required, personality)
    self.slot_menu.clear_menu()
    self.slot_name.set('')
    self.slot_type.set('')
    self.slot_label_id.set('')
    self.default_slot_value.set('')
    if 'SLOT_INFO' or 'SLOT_DESCRIPTION' or 'DEFAULT_SLOT_VALUE' in param_dict['PARAM_NAMES']:
      for index in xrange(slots_required):
        self.slot_menu.add_item('Slot %d' % index, 
                              lambda i=index: self._display_slot_info(i, param_dict))
    return

  def _set_display_invert(self, invert):
    '''
    Infternal Function, first function in the 'SetDisplayInvert' control flow.

    Args:
      state: int, see PIDDict.DISPLAY_INVERT for state name.
    '''
    self._controller.set_display_invert(invert)
    # self._controller.SetDisplayInvert(self.display_invert.get())

  def set_display_invert_complete(self, invert):
    if self.display_invert.get() != invert:
      self.display_invert.set(invert)

  def _set_pan_invert(self):
    '''
    Infternal Function, first function in the 'SetPanInvert' control flow.

    Args:
      state: boolean, true: inverted, false: normal.
    '''
    self._controller.SetPanInvert(self.pan_invert.get())

  def set_pan_invert_complete(self, invert):
    if self.pan_invert.get() != invert:
      self.pan_invert.set(invert)

  def _set_tilt_invert(self):
    '''
    Infternal Function, first function in the 'SetTiltInvert' control flow.

    Args:
      state: boolean, true: inverted, false: normal.
    '''
    self._controller.SetTiltInvert(self.tilt_invert.get())

  def set_tilt_invert_complete(self, invert):
    if self.tilt_invert.get() != invert:
      self.tilt_invert.set(invert)

  def _set_pan_tilt_swap(self):
    '''
    Infternal Function, irst function in the 'SetPanTiltSwap' control flow.

    Args:
      state: boolean, true: swapped, false: normal.
    '''
    self._controller.set_pan_tilt_swap(self.pan_tilt_swap.get())

  def set_pan_tilit_swap_complete(self, swap):
    if self.pan_tilt_swap.get() != swap:
      self.pan_tilt_swap.set(swap)

  def _set_language(self, language):
    self._controller.SetLanguage(language)

  def set_language_complete(self, language):
    if self.language_menu.get() != language:
      self.language_menu.set(language)

  def record_sensor(self, sensor_number):
    self._controller.record_sensor(sensor_number)

  def clear_sensor(self, sensor_number):
    self._controller.clear_sensor(sensor_number)

  # ============================================================================
  # ========================== Internal Methods ================================
  # ============================================================================

  def _tab_changed(self, event):
    '''
    Method bound to tab change event, calls self.update
    '''
    # Note that this will be called when the program starts
    self.update()

  def _grid_info(self, obj_list):
    """
    places the widgets subject to change upon completion of controlflows
    """
    obj_list.reverse()
    for r in xrange((len(obj_list) + 1) / 2):
      for c in xrange(2):
        obj_list.pop().grid(row=r, column=c)

  def _create_tab(self, tab_name, tab_label=None):
    """ Creates a tab. 

        will want to have all the options allowed by the ttk notebook widget to
        be args for this method

        Args:
          tab_name: string, cannot begin with a capital letter
          pid_list: list of strings, 
          tab_label: string that will be displayed on the tab, default set to 
            None, and tab_name will be on the tab

        Returns:
          tab: the Frame
    """
    if tab_label is None:
      tab_label = tab_name
    tab = tk.Frame(self._notebook, name=tab_name)
    self._notebook.add(tab, text=tab_label)
    return tab

  def _display_slot_info(self, slot_number, param_dict):
    """
    """
    self.slot_name.set('Name: %s' % 
        param_dict.get('SLOT_DESCRIPTION', {}).get('name', "N/A"))
    type_name = RDMConstants.SLOT_TYPE_TO_NAME[
          param_dict.get('SLOT_INFO', {})[slot_number].get('slot_type', "N/A")
          ].replace('_', ' ')
    self.slot_type.set('Type: %s' % type_name)

    if param_dict['SLOT_INFO'][slot_number]['slot_type'] != 0:
      self.slot_label_id.set('Primary Slot Index: %d' % param_dict.get(
                      'SLOT_INFO', {})[slot_number].get('slot_label_id', "N/A"))
    else:
      label_id = RDMConstants.SLOT_DEFINITION_TO_NAME[
        param_dict.get('SLOT_INFO', {})[slot_number].get('slot_label_id', "N/A")
        ].replace('_', ' ')
      self.slot_label_id.set('Slot Label: %s' % label_id)

    if 'DEFAULT_SLOT_VALUE' in param_dict:
      print param_dict['DEFAULT_SLOT_VALUE']
    self.default_slot_value.set('Default Slot Value: %d' %
                          param_dict.get('DEFAULT_SLOT_VALUE', {})[slot_number])

  def _display_personality_decription(self, slots_required, personality):
    self.slot_required.set("Slots Required: %s" % slots_required)
    self.personality_name.set("Personality ID: %s" % personality)

  def _get_personality_string(self, personality):
    return '%s (%d)' % (personality['name'], personality['slots_required'])

  def _populate_sensor_tab(self, sensor_number):
    self._controller.get_sensor_value(sensor_number)

  def display_sensor_data(self, param_dict, sensor_number):
    self.record_sensor_button.config(
        command = lambda: self.record_sensor(sensor_number), state = tk.NORMAL)
    self.clear_sensor_button.config(
        command = lambda: self.clear_sensor(sensor_number), state = tk.NORMAL)
    self.refresh_sensor_button.config(
        command = lambda: self._populate_sensor_tab(sensor_number), 
        state = tk.NORMAL)
    definition = param_dict['SENSOR_DEFINITION'][sensor_number]
    TYPE = RDMConstants.SENSOR_TYPE_TO_NAME[definition['type']].replace("_", " ")
    UNIT = RDMConstants.UNIT_TO_NAME[definition['unit']].replace("_", " ")
    PREFIX = RDMConstants.PREFIX_TO_NAME[definition['prefix']].replace("_", " ")
    self.sensor_type.set('Type: %s' % TYPE)
    self.sensor_unit.set('Unit: %s' % UNIT)
    self.sensor_prefix.set('Prefix: %s' % PREFIX)
    self.sensor_range.set('Range: %d - %d' % (definition['range_min'], 
                                               definition['range_max']))
    self.normal_range.set(
        'Normal Range: %d - %d' % 
        (definition['normal_min'], definition['normal_max']))
    self.supports_recording.set(
        'Supports Recording: %s' %
        bool(PIDDict.RECORDED_SUPPORTED & definition['supports_recording']))
    self.supports_lowest_highest.set('Supports Lowest/Highest: %s' %
        bool(PIDDict.LOWEST_HIGHEST_SUPPORTED & definition['supports_recording']))

    if 'SENSOR_VALUE' in param_dict:
      value = param_dict['SENSOR_VALUE'][sensor_number]
      self.present_value.set('Value: %d' % value['present_value'])
      self.lowest.set('Lowest Value: %d' % value['lowest'])
      self.highest.set('Highest Value: %d' % value['highest'])
      self.recorded.set('Recorded Value: %d' % value['recorded'])
