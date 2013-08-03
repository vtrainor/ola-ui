from ola.ClientWrapper import ClientWrapper, SelectServer
from ola.OlaClient import OlaClient, OLADNotRunningException
import threading
import time
from ola.RDMAPI import RDMAPI

class OLAThread(threading.Thread):
  """The thread which runs the OLA Client."""
  def __init__(self, pid_store):
    super(OLAThread,self).__init__()
    self._client=OlaClient()
    self._ss=None# created in run()
    self.daemon=True#allows the program to Terminate correctly
    self._pid_store=pid_store
    self._rdm_api=RDMAPI(self._client, self._pid_store)

  def run(self):
    """ creates a SelectServer object and runs it """
    self._ss=SelectServer()
    self._ss.AddReadDescriptor(self._client.GetSocket(),
                               self._client.SocketReady)
    print 'Starting the OLA event loop'
    self._ss.Run()
    print 'OLA thread finished'

  def stop(self):
    """ terminates SelectServer object (created in self.run()). """
    if self._ss is None:
      print 'OLAThread.Stop() called before thread was running'
      return
    print 'Stopping OLA thread'
    self._ss.Terminate()

  def run_discovery(self,universe,callback):
    """ runs discovery in specified universe
      
      Args:
        universe: int, specifies the universe in which to run discovery
        callback: method called upon discovery, takes two arguments(bool, [UID])
    
      Can be called from any thread.
      Callback is run in the OLA thread.
    """
    self._ss.Execute(lambda:self._run_discovery(universe,callback))

  def fetch_universes(self,callback):
    """ runs discovery in specified universe
      
      Args:
        universe: int, specifies the universe in which to run discovery
        callback: method called upon discovery, takes two arguments(bool, [UID])
    
      Can be called from any thread.
      Callback is run in the OLA thread.
    """
    self._ss.Execute(lambda:self._fetch_universes(callback))

  def rdm_get(self,universe,uid,sub_device,pid,callback,data=''):
    """ Executes, in the ola thread, an rdm inquiry. """
    # print "pid: %s" % pid
    # print "data %s" % data
    self._ss.Execute(lambda:self._rdm_get(universe,uid,sub_device,pid,
                                          callback,data))

  def rdm_set(self, universe, uid, sub_device, pid, callback, data):
    """ Executes, in the ola thread, the setting of an rdm variable. """
    print 'rdm set'
    self._ss.Execute(lambda:self._rdm_set(universe,uid,sub_device,pid,
                                          callback,data))

  def add_event(self, mili_secs, callback):
    """ creates an event that will happen after the specified number of mili 
        seconds.

        Args:
          mili_secs: the number of mili seconds before callback is called.
          callback: the function called on completion of the timer
    """
    self._ss.Execute(lambda: self._add_event(mili_secs, callback))

  def _add_event(self, mili_secs, callback):
    """
    """
    self._ss.AddEvent(mili_secs, callback)

  def _run_discovery(self, universe, callback):
    """ This method is only run in the OLA thread. """
    response=self._client.RunRDMDiscovery(universe,True,callback)
    if response==False:
      callback(False,[])

  def _fetch_universes(self, callback):
    """ This method is only run in the OLA thread. """
    response = self._client.FetchUniverses(callback)
    if response==False:
      callback([])

  def _rdm_get(self,universe,uid,sub_device,pid,callback,data):
    """ This method is only run in the OLA thread. """
    print "get %s" % pid
    self._rdm_api.Get(universe,uid,sub_device,self._pid_store.GetName(pid),
                      lambda r,d,e:self.complete_get(callback,r,d,e),data)
    # print "pid: %s" % pid
    # print "data: %s" % data
      
  def _rdm_set(self,universe,uid,sub_device,pid,callback,data):
    """ This method is only run in the OLA thread. """
    print '_rdm_set'
    self._rdm_api.Set(universe,uid,sub_device,self._pid_store.GetName(pid),
                      lambda r,d,e:self.complete_set(callback,r,d,e),data)

  def complete_get(self,callback,response,data,unpack_exception):
    """ Checks if the get was a success, calls the callback from run_get. """
    # need to do something with unpack_exception here
    if response.WasAcked()==False:
      callback(False,'')
    else:
      callback(True, data)

  def complete_set(self,callback,response,data,unpack_exception):
    """ Checks if the set was a success, calls the callback from run_set. """
    print 'RDM set completed'
    # need to do something with the unpack_exception here
    if response.WasAcked()==False:
      callback(False,str(unpack_exception))
    else:
      callback(True,data)

if __name__ == '__main__':
  print 'olathreading'