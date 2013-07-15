import Tkinter as tk
import simple_ui
import ttk

class RDMNotebook:
  def __init__(self, root, width=800, height=500,side=tk.TOP):
    """ Builds the ttk.Notebook """
    self.root = root
    self.cur_uid = None
    self.init_dx = width
    self.init_dy = height
    self.objects = []
    self.pid_index_dict = {}
    self._notebook = ttk.Notebook(self.root, name="nb", height=height, width=width)
    self.populate_defaults()
    # self.update_info_tab()
    self._notebook.pack(side=side)

  def populate_defaults(self):
    """ creates the default frames. """
    print "creating default tabs..."
    # create and populate the three default tabs
    self.info_tab = self.create_tab("info_tab", "Device Information")
    self._init_info()
    self.dmx_tab = self.create_tab("dmx_tab", "DMX")
    self._init_dmx()
    self.sensor_tab = self.create_tab("sensor_tab", "Sensors")
    self._init_sensor()
    self.pid_index_dict = {"DEVICE_INFO": [0,1,3,4,6,7,9,10,12,13,54,55,57,58,
                                           60,61,93,94],
                           "PRODUCT_DETAIL_ID_LIST": [15,16],
                           "DEVICE_MODEL_DESCRIPTION": [4],
                           "MANUFACTURER_LABEL": [18,19],
                           "DEVICE_LABEL": [2],
                           "FACTORY_DEFAULTS": [5],
                           "LANGUAGE_CAPABILITIES": [25],
                           "LANGUAGE": [24,25],
                           "SOFTWARE_VERSION_LABEL": [10],
                           "BOOT_SOFTWARE_VERSION_ID": [21,22],
                           "BOOT_SOFTWARE_VERSION_LABEL": [22],
                           "DMX_PERSONALITY": [61],
                           "DMX_PERSONALITY_DESCRIPTION": [64,65,67,68],
                           "DMX_START_ADDRESS": [55],
                           "SLOT_INFO": [69,70,71,73,74,76,77,79,80],
                           "SLOT_DESCRIPTION": [82,83,85,86],
                           "DEFAULT_SLOT_VALUE": [87,88,89,91,92],
                           "SENSOR_DEFINITION": [111,112,115,116,118,119,121,
                                                 122,124,125,127,128,130,131,
                                                 133,134,136,137,139,140],
                           "SENSOR_VALUE": [96,97,100,101,103,104,106,107,109,
                                            110],
                           "RECORD_SENSORS": [95],
                           "DEVICE_HOURS": [29],
                           "LAMP_HOURS": [28],
                           "LAMP_STRIKES": [32],
                           "LAMP_STATE": [30,31],
                           "LAMP_ON_MODE": [33,34],
                           "DEVICE_POWER_CYCLES": [36,37],
                           "DISPLAY_INVERT": [39,40],
                           "DISPLAY_LEVEL": [42,43],
                           "PAN_INVERT": [41],
                           "TILT_INVERT": [38],
                           "PAN_TILT_SWAP": [44],
                           "REAL_TIME_CLOCK": [8,11],
                           "RESET_DEVICE": [14],
                           "POWER_STATE": [45,46],
                           "PERFORM_SELFTEST": [48,49],
                           "SELF_TEST_DESCRIPTION": [50],
                           "CAPTURE_PRESET": [53],
                           "PRESET_PLAYBACK": [51,52] }

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

  def update_tabs(self, value, supported_pid):
    """
    """
    self._update_info(value, supported_pid)
    self._update_dmx(value, supported_pid)
    self._update_sensor(value, supported_pid)

  def act_objects(self, supported_pids):
    """
    """
    for widget in self.objects:
      widget.config(state = tk.DISABLED)
    for pid in supported_pids:
      for i in self.pid_index_dict[pid]:
        self.objects[i].config(state = tk.NORMAL)

  def _init_info(self):
    """ Initializes the parameters that will be in the info dictionary. """
    self.protocol_version = tk.StringVar(self.info_tab)
    self.device_label = tk.StringVar(self.info_tab)
    self.device_model = tk.StringVar(self.info_tab)
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.product_category = tk.StringVar(self.info_tab)
    self.real_time = tk.StringVar(self.info_tab)
    self.software_version = tk.StringVar(self.info_tab)
    self.sub_device_count = tk.StringVar(self.info_tab)
    self.product_ids = tk.StringVar(self.info_tab)
    self.manufacturer = tk.StringVar(self.info_tab)
    self.boot_software = tk.StringVar(self.info_tab)
    self.language = tk.StringVar(self.info_tab)
    self.languages = ["languages"]
    self.tilt_invert = tk.BooleanVar(self.info_tab)
    self.pan_invert = tk.BooleanVar(self.info_tab)
    self.pan_tilt_swap = tk.BooleanVar(self.info_tab)
    self.lamp_state = tk.StringVar(self.info_tab)
    self.lamp_states = ["lamp states"]
    self.device_hours = tk.StringVar(self.info_tab)
    self.lamp_on_mode = tk.StringVar(self.info_tab)
    self.lamp_on_modes = ["lamp on modes"]
    self.lamp_hours = tk.StringVar(self.info_tab)
    self.device_power_cycles = tk.StringVar(self.info_tab)
    self.lamp_strikes = tk.StringVar(self.info_tab)
    self.display_invert = tk.StringVar(self.info_tab)
    self.display_inverts = ["display inverts"]
    self.display_level = tk.StringVar(self.info_tab)
    self.power_state = tk.StringVar(self.info_tab)
    self.power_states = ["power states"]
    self.self_test_val = tk.StringVar(self.info_tab)
    self.self_test_vals = ["self test values"]
    self.self_test_desc = tk.StringVar(self.info_tab)
    self.preset_playback = tk.StringVar(self.info_tab)
    self.preset_playbacks = ["preset playbacks"]
    self.info_objects = [
                        tk.Label(self.info_tab, text="Protocol Version"),
                        tk.Label(self.info_tab,
                          textvariable=self.protocol_version),
                        tk.Entry(self.info_tab,
                          textvariable=self.device_label),
                         
                        tk.Label(self.info_tab, text="Device Model"),
                        tk.Label(self.info_tab,
                          textvariable=self.device_model),
                        tk.Checkbutton(self.info_tab, 
                          text = "Factory Defaults", 
                          variable = self.factory_defaults),
                         
                        tk.Label(self.info_tab, text="Product Category"),
                        tk.Label(self.info_tab,
                          textvariable=self.product_category),
                        tk.Label(self.info_tab, textvariable=self.real_time),
                         
                        tk.Label(self.info_tab, text="Software Version"),
                        tk.Label(self.info_tab, 
                          textvariable=self.software_version),
                        tk.Button(self.info_tab, text="Update Clock"),
                         
                        tk.Label(self.info_tab, text="Sub-Device Count"),
                        tk.Label(self.info_tab,
                          textvariable=self.sub_device_count),
                        tk.Button(self.info_tab, text="Reset Device"),
                         
                        tk.Label(self.info_tab, text="Product IDs"),
                        tk.Label(self.info_tab, 
                          textvariable=self.product_ids),
                        tk.Label(self.info_tab, text=""),
                         
                        tk.Label(self.info_tab, text="Manufacturer"),
                        tk.Label(self.info_tab, 
                          textvariable=self.manufacturer),
                        tk.Label(self.info_tab, text=""),
                         
                        tk.Label(self.info_tab, text="Boot Software"),
                        tk.Label(self.info_tab, 
                          textvariable=self.boot_software),
                        tk.Label(self.info_tab, text=""),
                         
                        tk.Label(self.info_tab, text="Language"),
                        tk.OptionMenu(self.info_tab, self.language, 
                          *self.languages),
                        tk.Label(self.info_tab, text=""),
                         
                        tk.Checkbutton(self.info_tab, text="Tilt Invert", 
                          variable = self.tilt_invert),
                        tk.Checkbutton(self.info_tab, text="Pan Invert", 
                          variable = self.pan_invert),
                        tk.Checkbutton(self.info_tab, text="Pan Tilt Swap", 
                          variable = self.pan_tilt_swap),

                        tk.Label(self.info_tab, text="Lamp State"),
                        tk.OptionMenu(self.info_tab, self.lamp_state,
                          *self.lamp_states),
                        tk.Label(self.info_tab, 
                          textvariable=self.device_hours),

                        tk.Label(self.info_tab, text="Lamp on Mode"),
                        tk.OptionMenu(self.info_tab, self.lamp_on_mode,
                          *self.lamp_on_modes),
                        tk.Label(self.info_tab, textvariable=self.lamp_hours),
                         
                        tk.Label(self.info_tab, text="Device Power Cycles"),
                        tk.Label(self.info_tab, 
                          textvariable=self.device_power_cycles),
                        tk.Label(self.info_tab, 
                          textvariable=self.lamp_strikes),
                         
                        tk.Label(self.info_tab, text="Display Invert"),
                        tk.OptionMenu(self.info_tab, self.display_invert, 
                          *self.display_inverts),
                        tk.Label(self.info_tab, text=""),

                        tk.Label(self.info_tab, text="Display Level"),
                        tk.Label(self.info_tab, 
                          textvariable=self.display_level),
                        tk.Label(self.info_tab, text=""),

                        tk.Label(self.info_tab, text="Power State"),
                        tk.OptionMenu(self.info_tab, self.power_state, 
                          *self.power_states),
                        tk.Label(self.info_tab, text=""),

                        tk.Button(self.info_tab, text="Preform Self-Test"),
                        tk.OptionMenu(self.info_tab, self.self_test_val, 
                          *self.self_test_vals),
                        tk.Label(self.info_tab, 
                          textvariable=self.self_test_desc),

                        tk.Label(self.info_tab, text=""),
                        tk.OptionMenu(self.info_tab, self.preset_playback, 
                          *self.preset_playbacks),
                        tk.Button(self.info_tab, text="Capture Preset")
                       ]
    for widget in self.info_objects:
        self.objects.append(widget)
    self._grid_info(self.info_objects)

  def _init_dmx(self):
    """ Initializes the parameters that will be in the dmx dictionary. """
    self.dmx_start_address = tk.StringVar(self.dmx_tab)
    self.dmx_footprint = tk.StringVar(self.dmx_tab)
    self.dmx_personality = tk.StringVar(self.dmx_tab)
    self.dmx_personalities = ["dmx personalities"]
    self.personality_name = tk.StringVar(self.dmx_tab)
    self.slots_required = tk.StringVar(self.dmx_tab)
    self.dmx_slot = tk.StringVar(self.dmx_tab)
    self.dmx_slots = ["dmx slots"]
    self.offset = tk.StringVar(self.dmx_tab)
    self.slot_type = tk.StringVar(self.dmx_tab)
    self.slot_label_id = tk.StringVar(self.dmx_tab)
    self.slot_number = tk.StringVar(self.dmx_tab)
    self.slot_name = tk.StringVar(self.dmx_tab)
    self.default_slot_offset = tk.StringVar(self.dmx_tab)
    self.default_slot_value = tk.StringVar(self.dmx_tab)
    self.dmx_objects = [
                        tk.Label(self.dmx_tab, text="Start Address:"),
                        tk.Entry(self.dmx_tab, 
                          textvariable=self.dmx_start_address),
                        tk.Label(self.dmx_tab, text=""),

                        tk.Label(self.dmx_tab, text="DMX Footprint:"),
                        tk.Label(self.dmx_tab, 
                          textvariable=self.dmx_footprint),
                        tk.Label(self.dmx_tab, text=""),
                        
                        tk.Label(self.dmx_tab, text="Current Personality:"),
                        tk.OptionMenu(self.dmx_tab, self.dmx_personality,
                          *self.dmx_personalities),
                        tk.Label(self.dmx_tab, text=""),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Personality Name:"),
                        tk.Label(self.dmx_tab,
                          textvariable=self.personality_name),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slots Required:"),
                        tk.Label(self.dmx_tab,
                          textvariable=self.slots_required),

                        tk.Label(self.dmx_tab, text="Slot Info:"),
                        tk.Label(self.dmx_tab, text="Choose Slot"),
                        tk.OptionMenu(self.dmx_tab, self.dmx_slot, 
                          *self.dmx_slots),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Offset:"),
                        tk.Label(self.dmx_tab, textvariable=self.offset),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slot Type:"),
                        tk.Label(self.dmx_tab, textvariable=self.slot_type),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slot Label ID:"),
                        tk.Label(self.dmx_tab, textvariable=self.slot_label_id),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slot Number:"),
                        tk.Label(self.dmx_tab, textvariable=self.slot_number),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slot Name:"),
                        tk.Label(self.dmx_tab, textvariable=self.slot_name),

                        tk.Label(self.dmx_tab, text="Default Slot:"),
                        tk.Label(self.dmx_tab, text="Offset:"),
                        tk.Label(self.dmx_tab,
                          textvariable=self.default_slot_offset),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, text="Slot Value"),
                        tk.Label(self.dmx_tab,
                          textvariable=self.default_slot_value)
                       ]
    for widget in self.dmx_objects:
        self.objects.append(widget)
    self._grid_info(self.dmx_objects)

  def _init_sensor(self):
    """ Initializes the paramters that will be in the device monitoring 
        dictionary.
    """
    self.sensor_count = tk.StringVar(self.sensor_tab)
    self.sensor_info = tk.StringVar(self.dmx_tab)
    self.sensors = ["sensors"]
    self.present_value = tk.StringVar(self.dmx_tab)
    self.lowest_value = tk.StringVar(self.dmx_tab)
    self.highest_value = tk.StringVar(self.dmx_tab)
    self.recorded_value = tk.StringVar(self.dmx_tab)
    self.sensor_desc = tk.StringVar(self.dmx_tab)
    self.sensor_type = tk.StringVar(self.dmx_tab)
    self.sensor_unit = tk.StringVar(self.dmx_tab)
    self.sensor_prefix = tk.StringVar(self.dmx_tab)
    self.range_min = tk.StringVar(self.dmx_tab)
    self.range_max = tk.StringVar(self.dmx_tab)
    self.norm_min = tk.StringVar(self.dmx_tab)
    self.norm_max = tk.StringVar(self.dmx_tab)
    self.recording = tk.StringVar(self.dmx_tab)
    self.sensor_name = tk.StringVar(self.dmx_tab)
    self.sensor_objects = [ 
                          tk.Label(self.sensor_tab, text="Sensor Count:"),
                          tk.Label(self.dmx_tab,
                            textvariable=self.sensor_count),
                          tk.Button(self.sensor_tab, text="Record Sensors"),

                          tk.Label(self.sensor_tab, text="Choose Sensor:"),
                          tk.OptionMenu(self.sensor_tab, self.sensor_info,
                            *self.sensors),
                          tk.Label(self.sensor_tab, text=""),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Present Value:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.present_value),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Lowest Value:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.lowest_value),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Highest Value:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.highest_value),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Recorded Value:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.recorded_value),

                          tk.Label(self.sensor_tab, text="Choose Sensor:"),
                          tk.OptionMenu(self.sensor_tab, self.sensor_desc, 
                            *self.sensors),
                          tk.Label(self.sensor_tab, text=""),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Sensor Type:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.sensor_type),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Sensor Unit:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.sensor_unit),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Sensor Prefix:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.sensor_prefix),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Range Minimum:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.range_min),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Range Maximum"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.range_max),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Normal Minimum:"),
                          tk.Label(self.sensor_tab, textvariable=self.norm_min),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Normal Maximum:"),
                          tk.Label(self.sensor_tab, textvariable=self.norm_max),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Supports Recording:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.recording),

                          tk.Label(self.sensor_tab, text=""),
                          tk.Label(self.sensor_tab, text="Sensor Name:"),
                          tk.Label(self.sensor_tab,
                            textvariable=self.sensor_name)
                          ]
    for widget in self.sensor_objects:
      self.objects.append(widget)
    self._grid_info(self.sensor_objects)

  def _grid_info(self, obj_list):
    """
    """
    for i in range(len(obj_list)):
      if i%3 == 1:
        obj_list[i].config(width=35)
      else:
        obj_list[i].config(width=20)
    obj_list.reverse()
    for r in range((len(obj_list)+2)/3):
      for c in range(3):
        obj_list.pop().grid(row=r, column=c)

  def _display_info(self, frame, object_list):
    """ 
        Args:
          object_dict: (same as return from self._create_objects)
          frame: 
    """

  def _update_info(self, value, supported_pids):
    """ this function will allow me to update the tabs once the notebook has
        been intialized. Should work in a way similar to the _display_info 
        above. One way this could work is if 2 object dictionaries could
        relatively quickly be compared to each other and only where they differ
        would the objects be updated. The pid labels should never have to change
        except in tabs that are not the default three, i.e. in the manufacturer
        tab.

        Args:
          param_dict: dictionary, from the ui class, keys are supported 
            parameters and values are obtian from RDM get of key
    """
    print "updating"

    if "DEVICE_INFO" in supported_pids:
      self.protocol_version.set("%d.%d" % 
                                (value["protocol_major"], 
                                 value["protocol_minor"]))
      self.device_model.set(value["device_model"])
      self.product_category.set(value["product_category"])
      self.software_version.set(value["software_version"])
    elif "PRODUCT_DETAIL_ID_LIST" in supported_pids:
      id_list = []
      for d in value["detail_ids"]:
        id_list.append(d["detail_id"])
      self.product_ids.set(id_list)
    elif "DEVICE_MODEL_DESCRIPTION" in supported_pids:
      self.device_model.set("%s (%s)" % (value["description"],
                            self.device_model.get()))
    elif "MANUFACTURER_LABEL" in supported_pids:
      self.manufacturer.set(value["label"])
    elif "DEVICE_LABEL" in supported_pids:
      self.device_label.set(value["label"])
    elif "FACTORY_DEFAULTS" in supported_pids:
      self.factory_defaults.set(value["using_defaults"])
    elif "LANGUAGE_CAPABILITIES" in supported_pids:
      for d in value["languages"]:
        self.languages.append(d["language"])
    elif "LAMP_STRIKES" in supported_pids:
      self.lamp_strikes.set(value["strikes"])
    elif "SOFTWARE_VERSION_LABEL" in supported_pids:
      self.software_version_lab.set(value["label"])
    elif "LANGUAGE" in supported_pids:
      self.language.set(value["language"])
    elif "BOOT_SOFTWARE_VERSION" in supported_pids:
      self.boot_software_val.set(value["version"])
    elif "BOOT_SOFTWARE_LABEL" in supported_pids:
      self.boot_software_lab.set(value["label"])
    elif "DEVICE_HOURS" in supported_pids:
      self.device_hours.set(value["hours"])
    elif "POWER_STATE" in supported_pids:
      self.power_state.set(value["state"])
    elif "LAMP_STATE" in supported_pids:
      self.lamp_state.set(value["state"])
    elif "DEVICE_POWER_CYCLE" in supported_pids:
      self.device_power_cycles.set(value["power_cycles"])
    # # sets:
    # self.factory_default_callback = None
    # self.languages = ["languages"] 
    # self.lamp_on_modes = ["lamp on modes"]
    # self.powerstates = ["power states"]

  def _update_dmx(self, value, supported_pids):
    """ update tab """
    if "DEVICE_INFO" in supported_pids:
      self.dmx_personality.set(value["current_personality"])
      self.dmx_personalities = []
      for i in range(value["personality_count"]):
        self.dmx_personalities.append(i)
      self.dmx_start_address.set(value["dmx_start_address"])
    elif "DMX_PERSONALITY_DESCRIPTION" in supported_pids:
      self.personality_name.set(value["name"])
    #sets:
    # elif "DMX_PERSONALITY" in supported_pids:
    # elif "DMX_START_ADDRESS" in supported_pids:

  def _update_sensor(self, value, supported_pids):
    """
    """
    if "SENSOR_DEFINITION" in supported_pids:
        self.sensor_number.set(value["sensor_number"])
        self.sensor_type.set(value["type"])
        self.sensor_prefix.set(value["prefix"])

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