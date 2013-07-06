import Tkinter as tk
import ttk

class RDMNotebook:
  def __init__(self, root, width=800, height=500,side=tk.TOP):
    """ Builds the ttk.Notebook """
    self.root = root
    self.cur_uid = None
    self.init_dx = width
    self.init_dy = height
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
    self.dmx_tab = self.create_tab("dmx_tab",
                             "This will display the info from DMX related pids", 
                             "DMX")
    self.sensor_tab = self.create_tab("sensors", 
                          "This will display the info from sensor related pids",
                          "Sensors")

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

  def update_tabs(self, param_dict):
    """
    """
    self._update_info(param_dict)

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
                         tk.Label(self.info_tab, text=self.protocol_version),
                         tk.Checkbutton(self.info_tab, 
                           text = "Factory Defaults", 
                           variable = self.factory_defaults),
                         tk.Label(self.info_tab, text="Device Model"),
                         tk.Label(self.info_tab, text=self.device_model),
                         tk.Label(self.info_tab, text="will be entry box"),
                         tk.Label(self.info_tab, text="Product Category"),
                         tk.Label(self.info_tab, text=self.product_category),
                         tk.Button(self.info_tab, text="reset"),
                         tk.Label(self.info_tab, text="Manufacturer"),
                         tk.Label(self.info_tab, text=self.manufacturer),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Current Language"),
                         tk.Label(self.info_tab, text=self.language),
                         tk.OptionMenu(self.info_tab, self.language, 
                           *self.languages),
                         tk.Label(self.info_tab, text="Software Version"),
                         tk.Label(self.info_tab, 
                           text=self.software_version_val),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, 
                           text=self.software_version_lab),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Boot Software Version"),
                         tk.Label(self.info_tab, 
                           text=self.boot_software_val),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text=self.boot_software_lab),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Device Hours"),
                         tk.Label(self.info_tab, text=self.device_hours),
                         tk.OptionMenu(self.info_tab, self.lamp_on_mode,
                           *self.lamp_on_modes),
                         tk.Label(self.info_tab, text="Lamp Hours"),
                         tk.Label(self.info_tab, text=self.lamp_hours),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Lamp Strikes"),
                         tk.Label(self.info_tab, text=self.lamp_strikes),
                         tk.OptionMenu(self.info_tab, self.power_state, 
                           *self.power_states),
                         tk.Label(self.info_tab, text="Lamp State"),
                         tk.Label(self.info_tab, text=self.lamp_state),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Device Power Cycles"),
                         tk.Label(self.info_tab, text=self.device_power_cycles),
                         tk.Label(self.info_tab, 
                           text="Will be set widget for device power cycles"),
                         ]
    self._grid_info()

  def _init_dmx_dict():
    """ Initializes the parameters that will be in the dmx dictionary. """

  def _init_monitor_dict():
    """ Initializes the paramters that will be in the device monitoring 
        dictionary.
    """

  def _grid_info(self):
    """
    """
    print "griding..."
    for i in range(len(self.info_objects)):
      if i%3 == 1:
        print self.info_objects[i]
        self.info_objects[i].config(width=30)
      else:
        self.info_objects[i].config(width=20)
    objects = self.info_objects
    objects.reverse()
    for r in range((len(objects)+2)/3):
      for c in range(3):
        objects.pop().grid(row=r, column=c)

  def _display_info(self, frame, object_list):
    """ 
        Args:
          object_dict: (same as return from self._create_objects)
          frame: 
    """

  def _update_info(self, pid_dict,):
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
    self.protocol_version.set("%d.%d" % 
                              (pid_dict["DEVICE_INFO"]["protocol_major"], 
                               pid_dict["DEVICE_INFO"]["protocol_minor"]))
    self.factory_defaults.set(pid_dict["FACTORY_DEFAULTS"])
    self.device_model.set(pid_dict["DEVICE_INFO"]["device_model"])
    self.product_category.set(pid_dict["DEVICE_INFO"]["product_category"])
    self.manufacturer.set(pid_dict["MANUFACTURER_LABEL"])
    self.sofware_version_val.set(pid_dict["DEVICE_INFO"]["software_version"])
    self.software_version_lab.set(pid_dict["SOFTWARE_VERSION_LABEL"])
    self.language.set(pid_dict["LANGUAGE"])
    self.boot_software_val.set(pid_dict["BOOT_SOFTWARE_VERSION"])
    self.boot_software_lab.set(pid_dict["BOOT_SOFTWARE_LABEL"])
    self.device_hours.set(pid_dict["DEVICE_HOURS"])
    self.lamp_hours.set(pid_dict["LAMP_HOURS"])
    self.lamp_strikes.set(pid_dict["LAMP_STRIKES"])
    self.power_state.set(pid_dict["POWER_STATE"])
    self.lamp_state.set(pid_dict["LAMP_STATE"])
    self.device_power_cycles.set(pid_dict["DEVICES_POWER_CYCLES"])
    # sets:
    self.factory_default_callback = None
    self.languages = ["languages"] 
    self.lamp_on_modes = ["lamp on modes"]
    self.powerstates = ["power states"]

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