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
    self.create_tab('tab 1','hello')
    self.create_tab('tab 2', 'example text')

  def create_tab(self, tab_name, words, tab_label = None):
    """ Creates a tab. 

        will want to have all the options allowed by the ttk notebook widget to
        be args for this method

        Args:
          tab_name: string, cannot begin with a capital letter
          pid_list: list of strings, 
          tab_label: string that will be displayed on the tab, default set to 
            None, and tab_name will be on the tab
    """
    if tab_label is None:
        tab_label = tab_name
    # create each Notebook tab in a Frame
    tab = tk.Frame(self._notebook, name = tab_name)
    # here, instead of creating a Label, call self._display_info
    tk.Label(tab, text = words).pack( side = tk.LEFT)
    # Button to quit app on right
    btn = tk.Button(tab, text="quit", command = master.quit)
    btn.pack(side = tk.RIGHT)
    self._notebook.add(tab, text = tab_label) # add tab to Notebook

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
      if i <= len(object_dict)/2:
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
  root = tk.Tk() # create a top-level window

  master = tk.Frame(root, name='master', width = 200, heigh = 200)
  master.pack(fill=tk.BOTH) # fill both sides of the parent

  root.title('EZ') # title for top-level window

  nb = RDMNotebook(master)
  nb.main()