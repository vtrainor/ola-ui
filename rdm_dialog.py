import Tkinter as tk

class RDMDialog:

  def __init__ (self, parent, pid, value):
    print 'dialog init'
    self.top = tk.Toplevel(parent)
    self.pid = pid
    self.value = value
    tk.Label(self.top, text='RDM Dialog').pack()
    tk.Label(self.top, text='invalid value (%s) for %s' % (value, pid)).pack()
    tk.Button(self.top, text='Ok', command=self.ok).pack()


  def ok(self):
    self.top.destroy()