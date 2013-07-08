import Tkinter as tk
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
    print len(self.objects)
    self.dmx_tab = self.create_tab("dmx_tab", "DMX")
    self._init_dmx()
    print len(self.objects)
    self.sensor_tab = self.create_tab("sensors", 
                          "This will display the info from sensor related pids",
                          "Sensors")
    self.pid_index_dict = { "DEVICE_INFO": [0,1,3,4,6,7,15,16,42,43,48,49],
                            "FACTORY_DEFAULTS": [2],
                            "DEVICE_LABEL": [5],
                            "MANUFACTURER_LABEL": [9,10],
                            "LANGUAGE": [12,13,14],
                            "SOFTWARE_VERSION_LABEL": [19],
                            "BOOT_SOFTWARE_VERSION":[21,22],
                            "BOOT_SOFTWARE_LABEL": [25],
                            "DEVICE_HOURS": [27,28],
                            "LAMP_ON_MODE": [29],
                            "LAMP_HOURS": [30,31],
                            "LAMP_STRIKES": [33,34],
                            "POWER_STATE": [35],
                            "LAMP_STATE": [36,37],
                            "DEVICE_POWER_CYCLE": [39,40,41],
                            "DMX_PERSONALITY": [], #44
                            "PERSONALITY_DESCRIPTION": [46],
                            "DMX_START_ADDRESS": [50],
                            "DEVICE_MODEL_DESCRIPTION": [],
                            "DMX_PERSONALITY_DESCRIPTION":[],
                            "PRODUCT_DETAIL_ID_LIST": [],
                            "REAL_TIME_CLOCK":[]}

  def create_tab(self, tab_name, words, tab_label=None):
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

  def update_tabs(self, value, supported_pids):
    """
    """
    print len(self.objects)
    print supported_pids
    for widget in self.objects:
        widget.config(state = tk.DISABLED)
    self._update_info(value, supported_pids)
    self._update_dmx(value, supported_pids)
    for pid in supported_pids:
        for i in self.pid_index_dict[pid]:
          print i
          self.objects[i].config(state = tk.ACTIVE)

  def _init_info(self):
    """ Initializes the parameters that will be in the info dictionary. """
    print "init info"
    self.protocol_version = tk.StringVar(self.info_tab)
    self.factory_defaults = tk.BooleanVar(self.info_tab)
    self.factory_default_callback = None
    self.device_model = tk.StringVar(self.info_tab)
    self.product_category = tk.IntVar(self.info_tab)
    self.manufacturer = tk.StringVar(self.info_tab)
    self.software_version_val = tk.IntVar(self.info_tab)
    self.software_version_lab = tk.StringVar(self.info_tab)
    self.language = tk.StringVar(self.info_tab)
    self.boot_software_val = tk.IntVar(self.info_tab)
    self.boot_software_lab = tk.StringVar(self.info_tab)
    self.device_hours = tk.IntVar(self.info_tab)
    self.lamp_hours = tk.IntVar(self.info_tab)
    self.lamp_strikes = tk.IntVar(self.info_tab)
    self.power_state = tk.StringVar(self.info_tab)
    self.lamp_state = tk.StringVar(self.info_tab)
    self.device_power_cycles = tk.IntVar(self.info_tab)
    self.lamp_on_mode = tk.StringVar(self.info_tab)
    self.languages = ["languages"] 
    self.lamp_on_modes = ["lamp on modes"]
    self.power_states = ["power states"]
    self.info_objects = [tk.Label(self.info_tab, text="Protocol Version"),
                         tk.Label(self.info_tab, textvariable=self.protocol_version),
                         tk.Checkbutton(self.info_tab, 
                           text = "Factory Defaults", 
                           variable = self.factory_defaults),
                         
                         tk.Label(self.info_tab, text="Device Model"),
                         tk.Label(self.info_tab, textvariable=self.device_model),
                         tk.Label(self.info_tab, text="will be entry box"),
                         
                         tk.Label(self.info_tab, text="Product Category"),
                         tk.Label(self.info_tab, textvariable=self.product_category),
                         tk.Button(self.info_tab, text="reset"),
                         
                         tk.Label(self.info_tab, text="Manufacturer"),
                         tk.Label(self.info_tab, textvariable=self.manufacturer),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text="Current Language"),
                         tk.Label(self.info_tab, textvariable=self.language),
                         tk.OptionMenu(self.info_tab, self.language, 
                           *self.languages),
                         
                         tk.Label(self.info_tab, text="Software Version"),
                         tk.Label(self.info_tab, 
                           textvariable=self.software_version_val),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, 
                           textvariable=self.software_version_lab),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text="Boot Software Version"),
                         tk.Label(self.info_tab, 
                           textvariable=self.boot_software_val),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, textvariable=self.boot_software_lab),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text="Device Hours"),
                         tk.Label(self.info_tab, textvariable=self.device_hours),
                         tk.OptionMenu(self.info_tab, self.lamp_on_mode,
                           *self.lamp_on_modes),
                         
                         tk.Label(self.info_tab, text="Lamp Hours"),
                         tk.Label(self.info_tab, textvariable=self.lamp_hours),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text="Lamp Strikes"),
                         tk.Label(self.info_tab, textvariable=self.lamp_strikes),
                         tk.OptionMenu(self.info_tab, self.power_state, 
                           *self.power_states),
                         
                         tk.Label(self.info_tab, text="Lamp State"),
                         tk.Label(self.info_tab, textvariable=self.lamp_state),
                         tk.Label(self.info_tab, text=""),
                         
                         tk.Label(self.info_tab, text="Device Power Cycles"),
                         tk.Label(self.info_tab, textvariable=self.device_power_cycles),
                         tk.Label(self.info_tab, 
                           text="Will be set widget for device power cycles"),
                         ]
    for widget in self.info_objects:
        self.objects.append(widget)
    self._grid_info(self.info_objects)

  def _init_dmx(self):
    """ Initializes the parameters that will be in the dmx dictionary. """
    self.dmx_personality = tk.StringVar(self.dmx_tab)
    self.dmx_personalities = ["dmx personalities"]
    self.personality_des = tk.StringVar(self.dmx_tab)
    self.dmx_start_address = tk.IntVar(self.dmx_tab)
    self.dmx_objects = [tk.Label(self.dmx_tab, text="DMX Personality"),
                        tk.Label(self.dmx_tab, textvariable=self.dmx_personality),
                        tk.OptionMenu(self.dmx_tab, self.dmx_personality,
                          *self.dmx_personalities),

                        tk.Label(self.dmx_tab, text=""),
                        tk.Label(self.dmx_tab, textvariable=self.personality_des),
                        tk.Label(self.dmx_tab, text=""),
                        
                        tk.Label(self.dmx_tab, text="DMX Start Address"),
                        tk.Label(self.dmx_tab, textvariable=self.dmx_start_address),
                        tk.Label(self.dmx_tab, text=""),
                       ]
    for widget in self.dmx_objects:
        print widget
        self.objects.append(widget)
    self._grid_info(self.dmx_objects)

  def _init_monitor():
    """ Initializes the paramters that will be in the device monitoring 
        dictionary.
    """

  def _grid_info(self, obj_list):
    """
    """
    print "griding..."
    print "length: %d" % len(obj_list)
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

    if "MANUFACTURER_LABEL" in supported_pids:
      self.manufacturer.set(value["label"])
    elif "LAMP_STRIKES" in supported_pids:
      self.lamp_strikes.set(value["strikes"])
    elif "DEVICE_INFO" in supported_pids:
      self.protocol_version.set("%d.%d" % 
                                (value["protocol_major"], 
                                 value["protocol_minor"]))
      self.device_model.set(value["device_model"])
      self.product_category.set(value["product_category"])
      self.software_version_val.set(value["software_version"])
    elif "FACTORY_DEFAULTS" in supported_pids:
      self.factory_defaults.set(value["using_defaults"])
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
      self.personality_des.set(value["personality"])
    #sets:
    # elif "DMX_PERSONALITY" in supported_pids:
    # elif "DMX_START_ADDRESS" in supported_pids:

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