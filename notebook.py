import Tkinter as tk
import simple_ui
import ttk
import ola.RDMConstants as RDMConstants

class RDMNotebook:
  def __init__(self, root, controller, width=800, height=500, side=tk.TOP):
    """ Builds the ttk.Notebook """
    self.root = root
    self.controller = controller
    self.init_dx = width
    self.init_dy = height
    self.objects = {}
    self.pid_location_dict = {}
    self._notebook = ttk.Notebook(self.root, name="nb", height=height,
                                  width=width)

  def populate_defaults(self):
    """ creates the default frames. """
    print "creating default tabs..."
    # create and populate the three default tabs
    self.info_tab = self.create_tab("info_tab", "Device Information")
    self._init_info()
    self.dmx_tab = self.create_tab("dmx_tab", "DMX512 Setup")
    self._init_dmx()
    self.sensor_tab = self.create_tab("sensor_tab", "Sensors")
    self._init_sensor()
    self.setting_tab = self.create_tab("setting_tab", "Power and Lamp Settings")
    self._init_setting()
    self.config_tab = self.create_tab("config_tab", "Configuration")
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
    self.factory_defaults_button.config(command = self.rdm_set(
                              "FACTORY_DEFAULTS", self.factory_defaults.get()))
    self.start_address_entry.config(validatecommand = self.rdm_set(
                            "DMX_START_ADDRESS", self.dmx_start_address.get()))
    self.dmx_personality_menu.config(command = self.rdm_set(
                                "DMX_PERSONALITY", self.dmx_personality.get()))
    self.slot_menu.config(command = self.rdm_set(
                                            "SLOT_INFO",self.slot_number.get()))
    self.sensor_def.config(command = self.rdm_get(
                                "SENSOR_DEFINITION", self.sensor_number.get()))
    self.sensor_value.config(command = self.rdm_get(
                                      "SENSOR_VALUE", self.sensor_number.get()))
    self.lamp_state_menu.config(command = self.rdm_set(
                                            "LAMP_STATE",self.lamp_state.get()))
    self.lamp_on_mode_menu.config(command = self.rdm_set(
                                      "LAMP_ON_MODE", self.lamp_on_mode.get()))
    self.device_power_cycles_menu.config(command = self.rdm_set(
                        "DEVICE_POWER_CYCLES", self.device_power_cycles.get()))
    self.power_state_menu.config(command = self.rdm_set(
                                        "POWER_STATE", self.power_state.get()))
    self.language_menu.config(command = self.rdm_set(
                                              "LANGUAGE", self.language.get()))
    self.display_invert_menu.config(command = self.rdm_set(
                                  "DISAPLAY_INVERT",self.display_invert.get()))
    self.display_level_menu.config(command = self.rdm_set(
                                    "DISPLAY_LEVEL", self.display_level.get()))
    self.pan_invert_button.config(command = self.rdm_set(
                                          "PAN_INVERT", self.pan_invert.get()))
    self.tilt_invert_button.config(command = self.rdm_set(
                                        "TILT_INVERT", self.tilt_invert.get()))
    self.pan_tilt_swap_button.config(command = self.rdm_set(
                                    "PAN_TILT_SWAP", self.pan_tilt_swap.get()))
    for key in self.pid_location_dict.keys():
        self._grid_info(self.objects[key])
    self._notebook.pack(side=side)

  def create_tab(self, tab_name, tab_label=None):
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

  def set_callbacks(self, callback_get, callback_set):
    """
    """
    self.rdm_get = callback_get
    self.rdm_set = callback_set

  def update_tabs(self, value, pid):
    """ calls the update functions for the tab that the 

        Args:
          value: 
          pid:
    """
    if pid in self.pid_location_dict["PRODUCT_INFO"].keys():
      self._update_info(value, pid)
    elif pid in self.pid_location_dict["DMX512_SETUP"].keys():
      self._update_dmx(value, pid)
    elif pid in self.pid_location_dict["SENSORS"].keys():
      self._update_sensor(value, pid)
    elif pid in self.pid_location_dict["POWER_LAMP_SETTINGS"].keys():
      self._update_settings(value, pid)
    elif pid in self.pid_location_dict["CONFIGURATION"].keys():
      self._update_config(value, pid)

  def act_objects(self, supported_pids):
    """
    """
    # pass
    print "suppoerted_pids: %s" % supported_pids
    print "self.protocol_version: %s" % self.protocol_version.get()
    for key in self.objects.keys():
      for widget in self.objects[key]:
        widget.config(state = tk.DISABLED)
    for pid in supported_pids:
      if pid == "QUEUED_MESSAGE":
        pass
      elif pid in self.pid_location_dict["PRODUCT_INFO"].keys():
        print "objects: %s" % self.objects["PRODUCT_INFO"]
        for i in self.pid_location_dict["PRODUCT_INFO"][pid]:
          self.objects["PRODUCT_INFO"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["DMX512_SETUP"].keys():
        for i in self.pid_location_dict["DMX512_SETUP"][pid]:
          self.objects["DMX512_SETUP"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["SENSORS"].keys():
        for i in self.pid_location_dict["SENSORS"][pid]:
          self.objects["SENSORS"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["POWER_LAMP_SETTINGS"].keys():
        for i in self.pid_location_dict["POWER_LAMP_SETTINGS"][pid]:
          self.objects["POWER_LAMP_SETTINGS"][i].config(state = tk.NORMAL)
      elif pid in self.pid_location_dict["CONFIGURATION"].keys():
        for i in self.pid_location_dict["CONFIGURATION"][pid]:
          self.objects["CONFIGURATION"][i].config(state = tk.NORMAL)

  def _init_info(self):
    """
    """
    # Text Variables:
    self.protocol_version = tk.StringVar(self.info_tab)
    self.device_model = tk.StringVar(self.info_tab)
    self.product_category = tk.StringVar(self.info_tab)
    self.software_version = tk.StringVar(self.info_tab)
    self.sub_device_count = tk.StringVar(self.info_tab)
    self.product_dealtail_ids = tk.StringVar(self.info_tab)
    self.manufacturer_label = tk.StringVar(self.info_tab)
    self.device_label = tk.StringVar(self.info_tab)
    self.boot_software = tk.StringVar(self.info_tab)

    # Widgets:
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.factory_defaults_button = tk.Checkbutton(self.info_tab,
                                              variable = self.factory_defaults)

    self.objects["PRODUCT_INFO"] = [tk.Label(self.info_tab,
                                                     text = "Protocol Version"),
                            tk.Label(self.info_tab,
                                          textvariable = self.protocol_version),

                            tk.Label(self.info_tab, text = "Device Model"),
                            tk.Label(self.info_tab,
                                              textvariable = self.device_model),

                            tk.Label(self.info_tab, text = "Product Details:"),
                            tk.Label(self.info_tab,
                                          textvariable = self.product_category),

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
                                              textvariable = self.boot_software)
                            ]

  def _init_dmx(self):
    """
    """
    # Text Variables
    self.dmx_footprint = tk.StringVar(self.dmx_tab)
    self.dmx_start_address = tk.StringVar(self.dmx_tab)
    self.current_personality = tk.StringVar(self.dmx_tab)
    self.dmx_personality = tk.StringVar(self.dmx_tab)
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
    self.dmx_personality_menu = tk.OptionMenu(self.dmx_tab, 
                                                self.dmx_personality.get(), "")
    self.slot_menu = tk.OptionMenu(self.dmx_tab, self.slot_number.get(), "")

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
    self.sensor_def = tk.OptionMenu(self.sensor_tab,
                                                  self.sensor_number.get(), "")
    self.sensor_value = tk.OptionMenu(self.sensor_tab,
                                                  self.sensor_number.get(), "")

    self.objects["SENSORS"] = [tk.Label(self.sensor_tab,
                                                        text = "Choose Sensor"),
                              self.sensor_def,

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
                              self.sensor_value,

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
    self.device_power_cycles_menu = tk.OptionMenu(self.setting_tab,
                                            self.device_power_cycles.get(), "")
    self.power_state_menu = tk.OptionMenu(self.setting_tab,
                                                    self.power_state.get(), "")

    self.objects["POWER_LAMP_SETTINGS"] = [tk.Label(self.setting_tab,
                                                        text = "Device Hours:"),
                                          tk.Label(self.setting_tab,
                                              textvariable = self.device_hours),

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
                                                text = "Device Power Cycles:"),
                                          self.device_power_cycles_menu,

                                          tk.Label(self.setting_tab,
                                                        text = "Power State:"),
                                          self.power_state_menu
                                          ]

  def _init_config(self):
    """
    """
    # Variables
    self.language = tk.StringVar(self.config_tab)
    self.display_invert = tk.StringVar(self.config_tab)
    self.display_level = tk.StringVar(self.config_tab)
    self.pan_invert = tk.BooleanVar(self.config_tab)
    self.tilt_invert = tk.BooleanVar(self.config_tab)
    self.pan_tilt_swap = tk.BooleanVar(self.config_tab)
    self.real_time_clock = tk.StringVar(self.config_tab)

    # Widgets
    self.language_menu = tk.OptionMenu(self.config_tab, self.language, "")
    self.display_invert_menu = tk.OptionMenu(self.config_tab,
                                                  self.display_invert.get(), "")
    self.display_level_menu = tk.OptionMenu(self.config_tab,
                                                  self.display_level.get(), "")
    self.pan_invert_button = tk.Checkbutton(self.config_tab,
                          variable = self.pan_invert, 
                          text = "(what it means for the\nbutton to be checked")
    self.tilt_invert_button = tk.Checkbutton(self.config_tab)
    self.pan_tilt_swap_button = tk.Checkbutton(self.config_tab)


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

  def _grid_info(self, obj_list):
    """
    """
    for i in range(len(obj_list)):
      if i%2 == 1:
        obj_list[i].config(width=35)
      else:
        obj_list[i].config(width=20)
    obj_list.reverse()
    for r in range((len(obj_list)+1)/2):
      for c in range(2):
        obj_list.pop().grid(row=r, column=c)

  def _update_info(self, value, supported_pids):
    """
    """
    print "updating info"

    if "DEVICE_INFO" in supported_pids:
      self.protocol_version.set("%d.%d" % 
                                (value["protocol_major"], 
                                 value["protocol_minor"]))
      self.device_model.set(value["device_model"])
      self.product_category.set(value["product_category"])
      self.software_version.set(value["software_version"])
      self.sub_device_count.set(value["sub_device_count"])
    elif "PRODUCT_DETAIL_ID_LIST" in supported_pids:
      self.product_dealtail_ids.set(None)
      for d in value["detail_ids"]:
        if self.product_dealtail_ids.get() is None:
          self.product_dealtail_ids.set(d["detail_id"])
        else:
          self.product_dealtail_ids.set("%s, %s" % (
                                        self.product_dealtail_ids.get(),
                                        d["detail_id"]))
    elif "DEVICE_MODEL_DESCRIPTION" in supported_pids:
      self.device_model.set("%s (%s)" % (value["description"],
                            self.device_model.get()))
    elif "MANUFACTURER_LABEL" in supported_pids:
      self.manufacturer.set(value["label"])
    elif "DEVICE_LABEL" in supported_pids:
      self.device_label.set(value["label"])
    elif "FACTORY_DEFAULTS" in supported_pids:
      self.factory_defaults.set(value["using_defaults"])
    elif "SOFTWARE_VERSION_LABEL" in supported_pids:
      self.software_version.set("%s (%s)" % (value["label"], 
                                self.software_version.get()))
    elif "BOOT_SOFTWARE_VERSION_ID" in supported_pids:
      self.boot_software.set(value["version"])
    elif "BOOT_SOFTWARE_LABEL" in supported_pids:
      self.boot_software.set("%s (%s)" % (value["label"],
                                self.boot_software.get()))

  def _update_dmx(self, value, supported_pids):
    """
    """
    print "updating dmx"
    if "DEVICE_INFO" in supported_pids:
      self.dmx_footprint.set(value["dmx_footprint"])
      self.dmx_start_address.set(value["dmx_start_address"])
      self.dmx_personality.set("Personality %d of %d" % (
                                value["current_personality"],
                                value["personality_count"]))
    elif "DMX_PERSONALITY" in supported_pids:
      for i in range(value["personality_count"]):
        self.dmx_personality_menu["menu"].add_command(label = 
                      "Personality %d of %d" % (i, value["personality_count"]),
                      command = self.callback_dict["DMX_PERSONALITY"])
        self.personality_description_menu["menu"].add_command(label = 
                  "Personality %d of %d" % (i, value["personality_count"]),
                  command = self.callback_dict["DMX_PERSONALITY_DESCRIPTION"])
    elif "DMX_PERSONALITY_DESCRIPTION" in supported_pids:
      self.personality_name.set(value["name"])
      self.slots_required.set(value["slots_required"])
    elif "DMX_START_ADDRESS" in supported_pids:
      self.star_address_entry.config(
                      validatecommand = self.callback_dict["DMX_START_ADDRESS"])
    elif "SLOT_INFO" in supported_pids:
      print value
      self.slot_offset.set(value["slot_offset"])
      self.slot_type.set(value["slot_type"])
      self.slot_label_id.set(value["slot_label_id"])
    elif "SLOT_DESCRIPTION" in supported_pids:
      self.slot_number.set(value["slot_number"])
      self.slot_name.set(value["name"])
    elif "DEFAULT_SLOT_VALUE" in supported_pids:
      self.default_slot_offset.set(value["slot_offset"])
      self.default_slot_value.set(value["default_slot_value"])

  def _update_sensor(self, value, pid):
    """
    """
    if "DEVICE_INFO" in supported_pids:
      self.sensor_count.set(value["sensor_count"])
      # for i in range(self.sensor_count.get()):
      #   self.objects[97]["menu"].add_command( label = "sensor number %d" % i, 
      #             command = callback)
    elif "SENSOR_DEFINITION" in supported_pids:
      self.sensor_desc.set(value["sensor_number"])
      self.sensor_type.set(RDMConstants.SENSOR_TYPE_TO_NAME[value["type"]])
      self.sensor_prefix.set(value["prefix"])
      self.range_min.set(value["range_min"])
      self.range_max.set(value["range_max"])
      self.normal_min.set(value["normal_min"])
      self.normal_max.set(value["normal_max"])
      if value["supports_recording"]:
        self.supports_recording.set("Supported.")
      else:
        self.supports_recording.set("Not Supported")
      self.sensor_name.set(value["name"])
      self.sensor_unit.set(value["unit"])
    elif "SENSOR_VALUE" in supported_pids:
      print "sensor_value: %s" % value
      self.sensor_info.set(value["sensor_number"])
      self.present_value.set(value["present_value"])
      self.lowest_value.set(value["lowest"])
      self.highest_value.set(value["highest"])
      self.recorded_value.set(value["recorded"])

  def update_setting(self, value, pid):
    """
    """
    if "DEVICE_HOURS" in supported_pids:
      self.device_hours.set("%d Device Hours" % value["hours"])
    elif "LAMP_HOURS" in supported_pids:
      self.lamp_hours.set("%d Lamp Hours" % value["hours"])
    elif "LAMP_STRIKES" in supported_pids:
      self.lamp_strikes.set("%d Lamp Strikes" % value["strikes"])
    elif "POWER_STATE" in supported_pids:
      self.power_state.set(value["power_state"])
    elif "LAMP_STATE" in supported_pids:
      self.lamp_state.set(value["state"])
    elif "LAMP_ON_MODE" in supported_pids:

      self.lamp_on_mode.set([value["mode"]])
    elif "DEVICE_POWER_CYCLE" in supported_pids:
      self.device_power_cycles.set(value["power_cycles"])
    elif "DISPLAY_INVERT" in supported_pids:
      print "display invert: %s" % value
    elif "DISPLAY_LEVEL" in supported_pids:
      self.display_level.set(value["level"])
    elif "PAN_INVERT" in supported_pids:
      self.pan_invert.set(value["invert"])
    elif "TILT_INVERT" in supported_pids:
      self.tilt_invert.set(value["invert"])
    elif "PAN_TILT_SWAP" in supported_pids:
      self.pan_tilt_swap.set(value["swap"])
    elif "REAL_TIME_CLOCK" in supported_pids:
      self.real_time.set("%d/%d/%d at %d:%d:%d" % (value["month"], value["day"],
                        value["year"], value["hour"], value["minute"],
                        value["second"]))
    elif "POWER_STATE" in supported_pids:
      self.power_state.set(value["power_state"])
    elif "SELF_TEST_DESCRIPTION" in supported_pids:
      self.self_test_val.set(value["test_number"])
      self.self_test_desc.set(value["description"])
    elif "PRESET_PLAYBACK" in supported_pids:
      self.preset_playback.set("%s (%d)" % (value[label][value["mode"]],
                              value["mode"]))

  def main(self):
    """ Main method for Notebook class. """
    self.root.mainloop()

  def Update(self):
    # TODO 9: based on the current selected tab, call one of:
    # GetBasicInformation()
    # GetDmxInformation()
    # GetSensorInformation()
    pass

  def RenderBasicInformation(self, param_dict):
    # Given a dict with the device label, manufacturer label etc.
    # update the widgets on the info tab
    print "param_dict: %s" % param_dict
    pass

  def RenderDmxInformation(self, params):
    pass

  def RenderSensorInformation(self, params):
    pass


if __name__ == "__main__":
  ui = simple_ui.DisplayApp()

  master = tk.Frame(root, name="master", width = 200, heigh = 200)
  master.pack(fill=tk.BOTH) # fill both sides of the parent

  root.title("EZ") # title for top-level window

  nb = RDMNotebook(master, ui)
  nb.main()
