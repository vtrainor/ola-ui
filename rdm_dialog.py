import Tkinter as tk

class RDMDialog:
  """Dialog class for failed RDM messages.

  This class alerts the user to any errors that may have occured in the ola
  thread. The class is accessed from the simple_ui file.
  """

  def __init__ (self, parent, error):
    self.top = tk.Toplevel(parent)
    tk.Label(self.top, text='RDM Dialog').pack()
    tk.Label(self.top, text=error).pack()
    tk.Button(self.top, text='Ok', command=self.ok).pack()


  def ok(self):
    """ Destroys the Dialog window.
    called when the user clicks the Tkinter button on the window.
    """
    self.top.destroy()