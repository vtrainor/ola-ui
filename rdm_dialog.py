import Tkinter as tk

class RDMDialog:

  def __init__ (self, parent, error):
    print 'dialog init'
    self.top = tk.Toplevel(parent)
    tk.Label(self.top, text='RDM Dialog').pack()
    tk.Label(self.top, text=error).pack()
    tk.Button(self.top, text='Ok', command=self.ok).pack()


  def ok(self):
    self.top.destroy()