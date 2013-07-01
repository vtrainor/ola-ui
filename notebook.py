import Tkinter as tk
import ttk

class RDMNotebook:
  def __init__(self, master, width=600, height=400):
    """ Builds the ttk.Notebook """
    self.root = master
    self.init_dx = width
    self.init_dy = height
    self._notebook = ttk.Notebook(self.root, name = 'nb')
    self.populate_tabs()
    self._notebook.pack()

  def populate_tabs(self):
    """ creates the default frames. """
    print 'creating default tabs...'
    self.info_tab = self.create_tab('info_tab',
                            'This will display the info device monitoring pids', 
                            'Device Information')
    self.dmx_tab = self.create_tab('dmx_tab',
                             'This will display the info from DMX related pids', 
                             'DMX')
    self.sensor_tab = self.create_tab('sensors', 
                          'This will display the info from sensor related pids',
                          'Sensors')

  def create_tab(self, tab_name, words, tab_label = None):
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

  def update_tabs(self, supported_params):
    """ to update the tabs this function will call the rdm_gets on all supported
        parameters and in the callback function the current data dictionary
        (which has yet to be created) will be updated with the latest data.
        After that I will be able to call create objects and display info.
        For the sake of efficiency I think it would work best if the objects
        dictionary held as many widgets that use tk variables as possible so
        that the variable can be changed and the objects won't have to be
        re-packed over and over again. The tk variables are the intVar, 
        stringVar, and boolVar so that should cover most things.
    """
    pass
    # # the following code was copy and pasted from simple_ui and has not yet been
    # # edited to work within the notebook class.
    # for item in pid_list:
    #   print item
    #   pid = self._pid_store.GetPid(item["param_id"], uid.manufacturer_id).name
    #   if pid is not None:
    #     print "pid: %s"%pid
    #     # will either have to make a series of elifs here for pids that take pds
    #     # or will have to come up with a different system for dealing with this
    #     # kind of pid
    #     if pid == "DMX_PERSONALITY_DESCRIPTION":
    #       data = [1]
    #     else:
    #       data = []
    #     self.ola_thread.rdm_get(self.universe.get(), uid, 0, pid, 
    #            lambda b, s, uid = uid:self._get_value_complete(uid, b, s), data)
    #   elif pid is None:
    #     # look up how to handle manufactuer pids
    #     # need to be able to:
    #     #   1. get the value for the pid
    #     #   2. figure out what kind of widget I need to display this information

  def _create_objects(self, tab, supported_pids):
    """ creates a dictionary of all pids that are assigned to the frame, tab.

        Hand coded for pids

        Returns:
          dictionary of string keys and values that are tuples of 2 objects. the
          first object will display the information returned by the rdm get and
          the second will either be a blank label of a certian length or some 
          form of an entry box widget, linked to a rdm set.
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

  def _update_display(self):
    """ this function will allow me to update the tabs once the notebook has
        been intialized. Should work in a way similar to the _display_info 
        above. One way this could work is if 2 object dictionaries could
        relatively quickly be compared to each other and only where they differ
        would the objects be updated. The pid labels should never have to change
        except in tabs that are not the default three, i.e. in the manufacturer
        tab.
    """

  def main(self):
    """ Main method for Notebook class. """
    self.root.mainloop()

if __name__ == '__main__':
  root = tk.Tk() # create a top-level window

  master = tk.Frame(root, name='master', width = 200, heigh = 200)
  master.pack(fill=tk.BOTH) # fill both sides of the parent

  root.title('EZ') # title for top-level window

  nb = RDMNotebook(master)
  nb.main()