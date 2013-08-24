import Tkinter as tk
from simple_ui import Controller

class Dialog:

  def __init__ (self, parent, pid, value):
    self.top = tk.Toplevel(parent)
    self.pid = pid
    self.value = value
    tk.Label(self.top, text='RDM Dialog')
    tk.Label(self.top, text='invalid value (%s) for %s' % (value, pid))
    self.button = tk.Button(self.top, text='Ok', command=self.ok)

  def ok(self):
    self.top.destroy()