import Tkinter as tk
import ttk

class RDMNotebook:
  def __init__(self, master, width=600, height=400):
    """ Builds the ttk.Notebook """
    self.root = master
    self._notebook = ttk.Notebook(self.root, width = self.init_dx,
                            height = (1/3)*self.init_dy)

  def populate_tabs():
    """ creates the default frames. """
    _dmx_tab = tk.Frame(self.root, name = '_dmx_tab')
    # determine pids that will be on this frame and specify them here.
    self._notebook.add(self.root, text = 'dmx information')

  def create_tab(self, tab_name, info_dict, pid_list):
    """ Creates a tab. 

        will want to have all the options allowed by the ttk notebook widget to
        be args for this method
    """
    tab = tk.Frame(self.root, name = tab_name)
    object_dict = []
    object_dict = self._create_objects(info_dict)
    notebook.add(tab,text = tab_name)

  def _create_objects(self, tab):
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
      if i <= len(object_dict)/2
        tk.Label(frame, text = key).grid(col = 0, row = i)
        object_dict[key][0].grid(col = 1, row = i)
        object_dict[key][1].grid(col = 2, row = i)
      else:
        tk.Label(frame, text = key).grid(col = 0, row = i-len(object_dict)/2)
        object_dict[key][0].grid(col=3, row = i-len(object_dict)/2)
        object_dict[key][1].grid(col=4, row = i-len(object_dict)/2)

  def main(self):
    """ Main method for Notebook class. """
    self.root.mainloop()

if __name__ == '__main__':
  nb=Notebook()
  nb.main()