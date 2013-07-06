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
    self._init_objects()
    self.info_tab = self.create_tab("info_tab",
                            "This will display the info device monitoring pids", 
                            "Device Information")
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
    tk.Label(tab, text = words).pack( side = tk.LEFT)
    self._notebook.add(tab, text = tab_label)
    return tab

  def update_info_tab(self, uid_data):
    """ updates all the widgets in the info tab. """
    pass

  def update_dmx_tab(self, uid_data):
    """ updates all the widgets in the dmx tab. """
    pass

  def update_sensor_tab(self, uid_data):
    """ updates all the widgets in the sensor tab. """
    pass
  
  def _init_info():
    """ Initializes the parameters that will be in the info dictionary. """
    self.procol_version = tk.StringVar(self.info_tab)
    self.factory_defaults = tk.BoolVar(self.info_tab)
    if factory_default_callback is None:
      # show that that parameter is not supported 
      pass
    self.device_model = tk.StringVar(self.info_tab)
    self.manufacturer = tk.StringVar(self.info_tab)
    self.software_version = tk.StringVar(self.info_tab)
    self.info_objects = [tk.Label(self.info_tab, text="Protocol Version"),
                         tk.Label(self.info_tab, text=self.protcol_version),
                         tk.CheckButton(self.info_tab, 
                           text = "Factory Defaults", 
                           variable = self.factory_defaults, 
                           command = factory_default_callback) 
                         tk.Label(self.info_tab, text="Device Model"),
                         tk.Label(self.info_tab, text=self.device_model),
                         tk.Label(self.info_tab, text="will be entry box"),
                         tk.Label(self.info_tab, text="Manufacturer"),
                         tk.Label(self.info_tab,text=self.manufacturer),
                         tk.Button(self.info_tab, text="reset"),
                         tk.Label(self.info_tab, text="Software Version"),
                         tk.Label(self,info_tab, text=self.sofware_version),
                         tk.Label(self.info_tab, text=""),
                         tk.Label(self.info_tab, text="Boot Software Version"),
                         tk.Label(self.info_tab, 
                           text="version %d" % self.boot_
                         ]

  def _init_dmx_dict():
    """ Initializes the parameters that will be in the dmx dictionary. """

  def _init_monitor_dict():
    """ Initializes the paramters that will be in the device monitoring 
        dictionary.
    """
    
  def _init_objects(self, factory_default_callback=None):
    """ creates a dictionary of all pids that are assigned to the frame, tab.

        Hand coded for pids

        Returns:
          object_list = [{param,(get_object, set_object)...}{...}{...}]
    """



  def _display_info(self, frame, object_dict):
    """ 
        Args:
          object_dict: (same as return from self._create_objects)
          frame: 
    """
    keys = object_dict.keys()
    for i in range(len(keys)):
      key = keys[i]
      if i <= len(object_dict)/2:
        tk.Label(frame, text = key).grid(col = 0, row = i)
        object_dict[key][0].grid(col = 1, row = i)
        object_dict[key][1].grid(col = 2, row = i)
      else:
        tk.Label(frame, text = key).grid(col = 0, row = i-len(object_dict)/2)
        object_dict[key][0].grid(col=3, row = i-len(object_dict)/2)
        object_dict[key][1].grid(col=4, row = i-len(object_dict)/2)

  def _update_info(self, param_dict):
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
    # want to look through the object/ widget dictionary and clear any values 
    # that are there.
    for key in param_dict:
      pass
      # create the object needed to be packed onto the tab, and put it in the 
      # object dictionary. 

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