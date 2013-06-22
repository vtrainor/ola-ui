from ola.ClientWrapper import ClientWrapper, SelectServer
from ola.OlaClient import OlaClient, OLADNotRunningException
import threading
import time
 
class OLAThread(threading.Thread):
  """The thread which runs the OLA Client."""
  def __init__(self):
    super(OLAThread, self).__init__()
    self._client = OlaClient()
    self._ss = None  # created in run()
    self.daemon = True
 
  def run(self):
    '''
    creates a SelectServer object and runs it
    '''
    self._ss = SelectServer()
    self._ss.AddReadDescriptor(self._client.GetSocket(),
                               self._client.SocketReady)
    print 'Starting the OLA event loop'
    self._ss.Run()
    print 'OLA thread finished'
 
  def Stop(self):
    '''
    terminates SelectServer object (created in self.run())
    '''
    if self._ss is None:
      print 'OLAThread.Stop() called before thread was running'
      return
 
    print 'Stopping OLA thread'
    self._ss.Terminate()       
                                                                                                                               
  def RunDiscovery(self, universe, callback):
    '''
    Can be called from any thread.
    Callback takes two arguments(bool, [UID])
    Callback is run in the OLA thread.
    '''
    self._ss.Execute(lambda : self._RunDiscovery(universe, callback))                                                                                                                            
 
  def Execute(self, cb):
    print 'calling execute'
    self._ss.Execute(cb)
 
  def _RunDiscovery(self, universe, callback):
    '''
    This method is only run in the OLA thread.
    '''
    response = self._client.RunRDMDiscovery(universe, True, callback)
    if response == False:
      callback( False, [] )
    
  def RDMGet(self, universe, uid, sub_device, pid, callback, data = ''):
    '''
    
    '''
    print 'rdm get'
    self._ss.Execute(lambda: self._RDMGet(universe, uid, sub_device, pid, callback, data) )
    
  def _RDMGet(self, universe, uid, sub_device, pid, callback, data):
    '''
    This method is only run in the OLA thread.
    '''
    print '_rdm_get'
    self._client.RDMGet(universe, uid, sub_device, pid, lambda r: self.CompleteGet(callback, r), data)
      
  def CompleteGet(self, callback, response):
    '''
    
    '''
    print 'RDM get completed'
    if response.WasAcked() == False:
    	callback(False, '')
    else: 
      callback( True, response.data )
    
if __name__ == '__main__':
  print 'olathreading'