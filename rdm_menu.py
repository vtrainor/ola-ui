#!/opt/local/bin/python2.7

import Tkinter as tk

class RDMMenu(object):
  def __init__(self, master, empty_label, full_label):
    self.root = master
    self.empty_label = empty_label
    self.full_label = full_label

    self.variable = tk.StringVar(self.root)
    self.menu = tk.OptionMenu(self.root, self.variable, '')
    
    self.clear_menu()
    
  def get(self):
  	return self.variable.get()
    
  def pack(self, *args, **kwargs):
  	self.menu.pack(*args, **kwargs)
  	
  def grid(self, *args, **kwargs):
  	self.menu.grid(*args, **kwargs)
  

  def clear_menu(self):
    self.variable.set(self.empty_label)
    self.menu["menu"].delete(0, tk.END)
    self.menu.configure(state=tk.DISABLED)

  def add_item(self, item, command):
    if self.menu['menu'].index('end') is None:
      # If there was nothing in the menu, we enable it and set the text
      self.menu.configure(state=tk.NORMAL)
      self.variable.set(self.full_label)

    self.menu["menu"].add_command(
      label = item,
      command = lambda:self.item_selected(item, command))
    return self.menu['menu'].index(tk.END)

  def item_selected(self, item, command):
    print 'Item selected %s' % item
    self.variable.set(item)
    command()
    
  def config(self, *args, **kwargs):
  	self.menu.config(*args, **kwargs)