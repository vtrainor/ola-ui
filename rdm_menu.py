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
    '''
    Returns:
      current string value of the StringVar
    '''
    return self.variable.get()
    
  def set(self, value):
    '''
    sets the string var to value
    '''
    print "setting to: %s" % value
    self.variable.set(value)
    self.root.update_idletasks()
    
  def pack(self, *args, **kwargs):
    '''
    see tkinter pack
    '''
    self.menu.pack(*args, **kwargs)
    
  def grid(self, *args, **kwargs):
    '''
    see tkinter grid
    '''
    self.menu.grid(*args, **kwargs)
  

  def clear_menu(self):
    '''
    clears and disables the menu
    '''
    self.variable.set(self.empty_label)
    self.menu["menu"].delete(0, tk.END)
    self.menu.configure(state=tk.DISABLED)

  def add_item(self, item, command):
    '''
    add item to the option menu

    Args:
      item: the label to go on the option menu
      command: the command to be called when the item is selected
    '''
    if self.menu['menu'].index('end') is None:
      # If there was nothing in the menu, we enable it and set the text
      self.menu.configure(state=tk.NORMAL)
      self.variable.set(self.full_label)

    self.menu["menu"].add_command(
        label = item,
        command = lambda:self.item_selected(item, command))
    return self.menu['menu'].index(tk.END)

  def item_selected(self, item, command):
    '''
    sets the text variable of the option menu and calls the command specified in
    add_command.

    Args: 
      item: the string that the StringVar associated with the OptionMenu will be
            set to.
      command: the command called when the item is selected, usually is a
               trigger to an RDM get or RDM set
    '''
    print 'Item selected %s' % item
    self.variable.set(item)
    command()

  def entryconfigure(self, index, *args, **kwargs):
    '''
    Configures the item at the given index, uses the key word arguments of 
    tkinter widget config.

    Args:
      index: index of item to configure.
    '''
    self.menu['menu'].entryconfigure(index, *args, **kwargs)
    
  def config(self, *args, **kwargs):
    '''
    Configure for the OptionMenu
    '''
    self.menu.config(*args, **kwargs)