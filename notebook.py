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
    # create and populate the three default tabs
    self.info_tab = self._create_tab("info_tab", "Device Information")
    self._init_info()
    self.dmx_tab = self._create_tab("dmx_tab", "DMX512 Setup")
    self._init_dmx()
    self.sensor_tab = self._create_tab("sensor_tab", "Sensors")
    self._init_sensor()
    self.setting_tab = self._create_tab("setting_tab", "Power and Lamp Settings")
    self._init_setting()
    self.config_tab = self._create_tab("config_tab", "Configuration")
    self._init_config()
    self.pid_location_dict = {"PRODUCT_INFO": {"DEVICE_INFO": [0,1,2,3,4,5,6,7,
                                                              8,9],
                                      "PRODUCT_DETAIL_ID_LIST": [10,11],
                                      "DEVICE_MODEL_DESCRIPTION": [3],
                                      "MANUFACTURER_LABEL": [12,13],
                                      "DEVICE_LABEL": [14,15],
                                      "FACTORY_DEFAULTS": [16,17],
                                      "SOFTWARE_VERSION_LABEL": [7],
                                      "BOOT_SOFTWARE_VERSION_ID": [18,19],
                                      "BOOT_SOFTWARE_VERSION_LABEL": [19]
                              },
                              "DMX512_SETUP": {"DEVICE_INFO": [0,1,2,3,4,5],
                                      "DMX_PERSONALITY": [4,5],
                                      "DMX_PERSONALITY_DESCRIPTION": [4,5,6,7,
                                                                      8,9],
                                      "DMX_START_ADDRESS": [3],
                                      "SLOT_INFO": [10,11,13],
                                      "SLOT_DESCRIPTION": [10,11,15,17,19],
                                      "DEFAULT_SLOT_VALUE": [20,22,23]
                              },
                              "SENSORS": {"SENSOR_DEFINITION": [0,1,3,5,7,9,11,
                                                                13,15],
                                      "SENSOR_VALUE": [16,17,19,21,23,25,27],
                                      "RECORD_SENSORS": []
                              },
                              "POWER_LAMP_SETTINGS": {"DEVICE_HOURS": [0,1],
                                      "LAMP_HOURS": [2,3],
                                      "LAMP_STRIKES": [4,5],
                                      "LAMP_STATE": [6,7],
                                      "LAMP_ON_MODE": [8,9],
                                      "DEVICE_POWER_CYCLES": [10,11],
                                      "POWER_STATE": [12,13]
                              },
                              "CONFIGURATION": {"LANGUAGE_CAPABILITIES": [0,1],
                                      "LANGUAGE": [0,1],
                                      "DISPLAY_INVERT": [2,3],
                                      "DISPLAY_LEVEL": [4,5],
                                      "PAN_INVERT": [6,7],
                                      "TILT_INVERT": [8,9],
                                      "PAN_TILT_SWAP": [10,11],
                                      "REAL_TIME_CLOCK": [12,13]
                              }}
    for key in self.pid_location_dict.keys():
        self._grid_info(self.objects[key])
    self._notebook.pack(side = self.side)

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
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.factory_defaults_button = tk.Checkbutton(self.info_tab,
                                              variable = self.factory_defaults)
    
    self.device_label_button = tk.Button(self.info_tab, 
                                        text = "Update Device Label",
                                        command = self.device_label_set)
    self.objects["PRODUCT_INFO"] = [tk.Label(self.info_tab,
                                                     text = "RDM Protocol Version"),
                            tk.Label(self.info_tab,
                                          textvariable = self.protocol_version),

                            tk.Label(self.info_tab, text = "Device Model"),
                            tk.Label(self.info_tab,
                                              textvariable = self.device_model),

                            tk.Label(self.info_tab, text = "Product Category:"),
                            tk.Label(self.info_tab,
                                          textvariable = self.product_category),

                            tk.Label(self.info_tab, text = "Software Version:"),
                            tk.Label(self.info_tab,
                                          textvariable = self.software_version),

                            tk.Label(self.info_tab, text = "Product Details:"),
                            tk.Label(self.info_tab, 
                                        textvariable = self.product_detail_ids),

                            tk.Label(self.info_tab, text = "Sub-Device Count"),
                            tk.Label(self.info_tab,
                                          textvariable = self.sub_device_count),

                            tk.Label(self.info_tab, text = "Manufacturer:"),
                            tk.Label(self.info_tab,
                                        textvariable = self.manufacturer_label),

                            tk.Label(self.info_tab, text = "Device Label:"),
                            tk.Entry(self.info_tab,
                                              textvariable = self.device_label),

                            tk.Label(self.info_tab, text = "Factory Defaults:"),
                            tk.Checkbutton(self.info_tab,
                                              variable = self.factory_defaults),

                            tk.Label(self.info_tab,
                                              text = "Boot Software Version:"),
                            tk.Label(self.info_tab,
                                            textvariable = self.boot_software),

                            self.device_label_button,
                            tk.Label(self.info_tab, text = "")
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
    self.slot_offset = tk.StringVar(self.dmx_tab)
    self.slot_type = tk.StringVar(self.dmx_tab)
    self.slot_label_id = tk.StringVar(self.dmx_tab)
    self.default_slot_offset = tk.StringVar(self.dmx_tab)
    self.default_slot_value = tk.StringVar(self.dmx_tab)

    # Widgets
    self.start_address_entry = tk.Entry(self.dmx_tab,
                                          textvariable = self.dmx_start_address)
    self.dmx_personality_menu = RDMMenu(self.dmx_tab,
                                        "Personality description not supported.",
                                        "")
    self.slot_menu = RDMMenu(self.dmx_tab,
                             "No slot description.",
                             "Choose Slot")

    self.objects["DMX512_SETUP"] = [tk.Label(self.dmx_tab,
                                                      text = "DMX Footprint:"),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.dmx_footprint),

                                  tk.Label(self.dmx_tab,
                                                  text = "DMX Start Address:"),
                                  self.start_address_entry,

                                  tk.Label(self.dmx_tab,
                                                text = "Current Personality:"),
                                  self.dmx_personality_menu,

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.slot_required),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                          textvariable = self.personality_name),

                                  tk.Label(self.dmx_tab, text = "Slot Info:"),
                                  self.slot_menu,

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                                textvariable = self.slot_name),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                              textvariable = self.slot_offset),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                                textvariable = self.slot_type),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                            textvariable = self.slot_label_id),

                                  tk.Label(self.dmx_tab,
                                                      text = "Default Slot:"),
                                  tk.Label(self.dmx_tab,
                                    textvariable = self.default_slot_offset),

                                  tk.Label(self.dmx_tab, text = ""),
                                  tk.Label(self.dmx_tab,
                                        textvariable = self.default_slot_value)
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
    self.sensor_name = tk.StringVar(self.sensor_tab)
    self.sensor_number = tk.StringVar(self.sensor_tab)
    self.present_value = tk.StringVar(self.sensor_tab)
    self.lowest = tk.StringVar(self.sensor_tab)
    self.highest = tk.StringVar(self.sensor_tab)
    self.recorded = tk.StringVar(self.sensor_tab)

    # Widgets
    self.sensor_menu = RDMMenu(self.sensor_tab,
                                        "Sensor information not provided.",
                                        "Choose Sensor")

    self.objects["SENSORS"] = [tk.Label(self.sensor_tab,
                                                        text = "Choose Sensor"),
                              self.sensor_menu,

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_type),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_unit),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.sensor_prefix),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_range),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.normal_range),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                        textvariable = self.supports_recording),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                              textvariable = self.sensor_name),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.sensor_number),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                            textvariable = self.present_value),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                    textvariable = self.lowest),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                  textvariable = self.highest),

                              tk.Label(self.sensor_tab, text = ""),
                              tk.Label(self.sensor_tab,
                                                  textvariable = self.recorded)
                              ]

  def _init_setting(self):
    """
    """
    self.device_hours = tk.StringVar(self.setting_tab)
    self.lamp_hours = tk.StringVar(self.setting_tab)
    self.lamp_strikes = tk.StringVar(self.setting_tab)
    self.lamp_state = tk.StringVar(self.setting_tab)
    self.lamp_on_mode = tk.StringVar(self.setting_tab)
    self.device_power_cycles = tk.StringVar(self.setting_tab)
    self.power_state = tk.StringVar(self.setting_tab)

    # Widgets
    self.lamp_state_menu = tk.OptionMenu(self.setting_tab,
                                                      self.lamp_state.get(), "")
    self.lamp_on_mode_menu = tk.OptionMenu(self.setting_tab,
                                                    self.lamp_on_mode.get(), "")
    self.power_state_menu = tk.OptionMenu(self.setting_tab,
                                                    self.power_state.get(), "")

    self.objects["POWER_LAMP_SETTINGS"] = [tk.Label(self.setting_tab,
                                                        text = "Device Hours:"),
                                          tk.Label(self.setting_tab,
                                              textvariable = self.device_hours),

                                          tk.Label(self.setting_tab,
                                                text = "Device Power Cycles:"),
                                          tk.Label(self.setting_tab, 
                                            textvariable = self.device_power_cycles),

                                          tk.Label(self.setting_tab,
                                                          text = "Lamp Hours:"),
                                          tk.Label(self.setting_tab,
                                                textvariable = self.lamp_hours),

                                          tk.Label(self.setting_tab,
                                                        text = "Lamp Strikes:"),
                                          tk.Label(self.setting_tab,
                                              textvariable = self.lamp_strikes),

                                          tk.Label(self.setting_tab,
                                                          text = "Lamp State:"),
                                          self.lamp_state_menu,

                                          tk.Label(self.setting_tab,
                                                        text = "Lamp On Mode:"),
                                          self.lamp_on_mode_menu,

                                          tk.Label(self.setting_tab,
                                                        text = "Power State:"),
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
    self.language_menu = RDMMenu(self.config_tab, "Languages not supported.", "")
    self.display_invert_menu = tk.OptionMenu(self.config_tab,
                                            self.display_invert, 
                                            *PIDDict.DISPLAY_INVERT.values(),
                                            command = self._set_display_invert)
    self.display_level_menu = tk.Scale(self.config_tab, from_ = 0, to = 255, 
                                  variable = self.display_level,
                                  orient = tk.HORIZONTAL,
                                  command = self._controller.SetDisplayLevel,
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
    self.pan_tilt_swap_button = tk.Checkbutton(self.config_tab,
                                               variable = self.pan_tilt_swap,
                                               command = self._set_pan_tilt_swap,
                                               state = tk.DISABLED)


    self.objects["CONFIGURATION"] = [tk.Label(self.config_tab,
                                                    text = "Device Language:"),
                                    self.language_menu,

                                    tk.Label(self.config_tab,
                                                      text = "Display Invert:"),
                                    self.display_invert_menu,

                                    tk.Label(self.config_tab, 
                                                      text = "Display Level:"),
                                    self.display_level_menu,

                                    tk.Label(self.config_tab,
                                                          text = "Pan Invert:"),
                                    self.pan_invert_button,

                                    tk.Label(self.config_tab,
                                                        text = "Tilt Invert:"),
                                    self.tilt_invert_button,

                                    tk.Label(self.config_tab,
                                                        text = "Pan Tilt Swap"),
                                    self.pan_tilt_swap_button,

                                    tk.Label(self.config_tab,
                                                      text = "Real Time Clock"),
                                    tk.Label(self.config_tab,
                                            textvariable = self.real_time_clock) 
                                   ]

  def device_label_set(self):
    """
    """
    self._controller.SetDeviceLabel(self.device_label.get())
  # ============================================================================
  # ============================== Update Tabs =================================
  # ============================================================================

  def Update(self):
    index = self._notebook.index('current')
    print 'The selected tab changed to %d' % index
    if index == 0:
      self._controller.GetBasicInformation()
    elif index == 1:
      self._controller.GetDMXInformation()
    elif index == 2:
      # get sensor name through sensor description 
      # for sensors 1 through sensor count,
      # then get sensor value when the user select sensor on menuy
      # add refresh button that triggers the control 
      # record sensor button (own pid) (takes sensor number)
      self._controller.GetSensorDefinitions()
    elif index == 3:
      self._controller.GetSettingInformation()
    elif index == 4:
      self._controller.GetConfigInformation()

  # ========================= Information Rendering ============================

  def RenderBasicInformation(self, param_dict):
    """
    """
    self.protocol_version.set("Version %d.%d" % (
                          param_dict["DEVICE_INFO"]["protocol_major"], 
                          param_dict["DEVICE_INFO"]["protocol_minor"]
                          ))
    self.device_model.set(param_dict["DEVICE_INFO"]["device_model"])
    self.device_model.set("%s (%d)" % (
                          param_dict.get("DEVICE_MODEL_DESCRIPTION", 'N/A'),
                          param_dict["DEVICE_INFO"]["device_model"]
                          ))
    index = param_dict["DEVICE_INFO"]["product_category"]
    self.product_category.set(RDMConstants.PRODUCT_CATEGORY_TO_NAME.get(index, 
    																											"").replace("_"," "))
    self.sub_device_count.set(param_dict["DEVICE_INFO"]["sub_device_count"])

    self.software_version.set("%s (%d)" % (
                          param_dict.get("SOFTWARE_VERSION_LABEL", "N/A"),
                          param_dict["DEVICE_INFO"]["software_version"]
                          ))
    self.sub_device_count.set(param_dict["DEVICE_INFO"]["sub_device_count"])
    if "PRODUCT_DETAIL_ID_LIST" in param_dict:
      ids = param_dict["PRODUCT_DETAIL_ID_LIST"]
      names = ', '.join(RDMConstants.PRODUCT_DETAIL_IDS_TO_NAME[id]
      																		 			for id in ids).replace("_", " ")
      self.product_detail_ids.set(names)
    self.manufacturer_label.set(param_dict.get("MANUFACTURER_LABEL", "N/A"))
    self.device_label.set(param_dict.get("DEVICE_LABEL", "N/A"))
    self.factory_defaults.set(param_dict.get("FACTORY_DEFAULTS", "N/A"))
      # self.factory_defaults_button(Checkbutton)
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
    return

  def RenderDMXInformation(self, param_dict):
    """
    """
    print "param_dict: %s" % param_dict
    device_info = param_dict["DEVICE_INFO"]
    self.dmx_personality_menu.clear_menu()
    self.slot_menu.clear_menu()
    self._display_personality_decription('N/A', 'N/A')
    if "DMX_PERSONALITY_DESCRIPTION" in param_dict:
      pers_desc = param_dict["DMX_PERSONALITY_DESCRIPTION"]
      for pers_id, data in param_dict["DMX_PERSONALITY_DESCRIPTION"].iteritems():
        self.dmx_personality_menu.add_item(self._get_personality_string(data),
                  lambda i = pers_id:self._controller.SetPersonality(i))
      personality = device_info['current_personality']
      self.dmx_personality_menu.set(self._get_personality_string(pers_desc[personality]))
      s = pers_desc[personality]['slots_required']
      p = personality
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
      pass
    # NOTE: Need to deal with this when the new Dummys are available with
    #       SLOT_INFO supported.
    #   slot_info = param_dict["SLOT_INFO"]
    #   for index in xrange(param_dict["DEVICE_INFO"]["dmx_footprint"]):
    #     self.slot_menu["menu"].add_item("Slot Number %d" % index,
    #             lambda index = index:self._display_slot_info(index, param_dict))
    # self.slot_offset.set(param_dict.get("SLOT_INFO", {}).get("slot_offset", "N/A"))
    # self.slot_type.set(param_dict.get("SLOT_INFO", {}).get("slot_type", "N/A"))
    # self.slot_label_id.set(param_dict.get("SLOT_INFO", {}).get("slot_label_id", "N/A"))
    # # I'm not sure how to deal with this pid...
    # self.default_slot_offset.set("N/A")
    # self.default_slot_value.set("N/A")
    print "DMX Rendered"

  def RenderSensorInformation(self, param_dict):
    '''
    2 dictionaries of values per sensor_number
      1. SENSOR_VALUE
      2. SENSOR_DEFINITION

    the sensor number will be sensor_menu.get()
    don't set the sensor_number upon rendering the tab
      -> wait for user input to display the sensor information
    '''
    # the display sensor info method should take 2 dictionaries
    # one for definition and one for value
    # these disctionaries should default to none
    # in sensor display create a check for if each dict is None
    # if that dictionary is None skip to next check
    # otherwise display  the information in that dict
    # then go to the next check
    # to _controller.GetSensorValue(index)
    print "rendering sensor information..."
    sensor_info = {}
    if 'SENSOR_DEFINITION' in param_dict:
      for index, sensor in param_dict['SENSOR_DEFINITION'].iteritems():
        sensor_name = sensor['name']
        self.sensor_menu.add_item('%s' % sensor_name,
                                lambda i=index: self._populate_sensor_tab(i))
    else: 
      self.sensor_menu.clear_menu()
      return

    # need second control flows for sensor tab 

    # if "DMX_PERSONALITY_DESCRIPTION" in param_dict:
    #   pers_desc = param_dict["DMX_PERSONALITY_DESCRIPTION"]
    #   for pers_id, data in param_dict["DMX_PERSONALITY_DESCRIPTION"].iteritems():
    #     self.dmx_personality_menu.add_item(self._get_personality_string(data),
    #               lambda i = pers_id:self._controller.SetPersonality(i))
    #   personality = device_info['current_personality']
    #   self.dmx_personality_menu.set(self._get_personality_string(pers_desc[personality]))
    #   s = pers_desc[personality]['slots_required']
    #   p = personality
    #   self._display_personality_decription(s, p)
   

  def RenderSettingInformation(self, param_dict):
    print "PARAM_DICT: %s" % param_dict
    self.device_hours.set(param_dict.get('DEVICE_HOURS', 'N/A'))
    self.lamp_hours.set(param_dict.get('LAMP_HOURS', 'N/A'))
    self.device_power_cycles.set(param_dict.get("DEVICE_POWER_CYCLES", "N/A"))
    self.lamp_strikes.set(param_dict.get('LAMP_STRIKES', 'N/A'))
    print "rendered"
    # if "LAMP_STATE" in param_dict:
    #   self.lamp_state = tk.StringVar(self.setting_tab)
    # if "LAMP_ON_MODE" in param_dict:
    #   self.lamp_on_mode = tk.StringVar(self.setting_tab)

    # if "POWER_STATE" in param_dict:
    #   self.power_state = tk.StringVar(self.setting_tab)

  def RenderConfigInformation(self, param_dict):
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
      self.display_invert.set(PIDDict.DISPLAY_INVERT.values()
                                                [param_dict['DISPLAY_INVERT']])
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
    print "Rendering Config...."

  # ============================================================================
  # ============================ RDM Set Methods ===============================
  # ============================================================================

  def PersonalityCallback(self, personality, param_dict):
    slots_required = param_dict.get("DMX_PERSONALITY_DESCRIPTION", 
                                    {})[personality].get(
                                    "slots_required", 
                                    "N/A")
    self._display_personality_decription(slots_required, personality)

  def _set_display_invert(self, invert):
    self._controller.SetDisplayInvert(invert)
    # self._controller.SetDisplayInvert(self.display_invert.get())

  def SetDisplayInvertComplete(self, invert):
    if self.display_invert.get() != invert:
      self.display_invert.set(invert)

  def _set_pan_invert(self):
    self._controller.SetPanInvert(self.pan_invert.get())

  def SetPanInvertComplete(self, invert):
    if self.pan_invert.get() != invert:
      self.pan_invert.set(invert)

  def _set_tilt_invert(self):
    self._controller.SetTiltInvert(self.tilt_invert.get())

  def SetTiltInvertComplete(self, invert):
    if self.tilt_invert.get() != invert:
      self.tilt_invert.set(invert)

  def _set_pan_tilt_swap(self):
    self._controller.SetPanTiltSwap(self.pan_tilt_swap.get())

  def SetPanTiltSwapComplete(self, swap):
    if self.pan_tilt_swap.get() != swap:
      self.pan_tilt_swap.set(swap)

  def _set_language(self, language):
    self._controller.SetLanguage(language)

  def SetLanguageComplete(self, language):
    if self.language_menu.get() != language:
      self.language_menu.set(language)

  # ============================================================================
  # ========================== Internal Methods ================================
  # ============================================================================

  def _tab_changed(self, event):
    '''
    Method bound to tab change evet, calls self.Update
    '''
    # Note that this will be called when the program starts
    self.Update()

  def _grid_info(self, obj_list):
    """
    places the widgets subject to change upon completion of controlflows
    """
    obj_list.reverse()
    for r in range((len(obj_list)+1)/2):
      for c in range(2):
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
    tab = tk.Frame(self._notebook, name = tab_name)
    self._notebook.add(tab, text = tab_label)
    return tab

  def _display_slot_info(self, slot_number, param_dict):
    """
    """
    self.slot_name.set(param_dict.get("SLOT_DESCRIPTION", {}).get(slot_number, "N/A"))

  def _display_personality_decription(self, slots_required, personality):
    self.slot_required.set("Slots Required: %s" % slots_required)
    self.personality_name.set("Personality ID: %s" % personality)

  def _display_sensor_information(self, sensor_dict):
    pass

  def _get_personality_string(self, personality):
    return '%s (%d)' % (personality['name'], personality['slots_required'])

  # def _set_display_level(self):
  #   level = self.display_level_menu.get()
  #   self._controller.SetDisplayLevel(level)
  def _populate_sensor_tab(self, sensor_number):
    self._controller.GetSensorValue(sensor_number)

  def DisplaySensorData(self, param_dict, sensor_number):
    definition = param_dict['SENSOR_DEFINITION'][sensor_number]
    TYPE = RDMConstants.SENSOR_TYPE_TO_NAME[definition['type']].replace("_", " ")
    UNIT = RDMConstants.UNIT_TO_NAME[definition['unit']].replace("_", " ")
    PREFIX = RDMConstants.PREFIX_TO_NAME[definition['prefix']].replace("_", " ")
    self.sensor_type.set('Type: %s' % TYPE)
    self.sensor_unit.set('Unit: %s' % UNIT)
    self.sensor_prefix.set('Prefix: %s' % PREFIX)
    self.sensor_range.set('Range: %d - %d' % (definition['range_min'], 
                                               definition['range_max']))
    self.normal_range.set('Normal Range: %d - %d' % (definition['normal_min'], 
                                               definition['normal_max']))
    self.supports_recording.set('Supports Recording: %s' %
                          PIDDict.SENSOR_VALUE[definition['supports_recording']]
                                               )
    if 'SENSOR_VALUE' in param_dict:
      value = param_dict['SENSOR_VALUE'][sensor_number]
      self.present_value.set('Value: %d' % value['present_value'])
      self.lowest.set('Lowest Value: %d' % value['lowest'])
      self.highest.set('Highest Value: %d' % value['highest'])
      self.recorded.set('Recorded Value: %d' % value['recorded'])

  def DisplayLevelCallback(self, level):
    if level != self.display_level_menu.get():
      pass
      # self.display_level_menu.set(level)
  # ============================== Main Loop ===================================

  def main(self):
    """ Main method for Notebook class. """
    self.root.mainloop()

if __name__ == "__main__":
  ui = simple_ui.DisplayApp()

  master = tk.Frame(root, name="master", width = 200, heigh = 200)
  master.pack(fill=tk.BOTH) # fill both sides of the parent

  root.title("EZ") # title for top-level window

  nb = RDMNotebook(master, ui)
  nb.main()
