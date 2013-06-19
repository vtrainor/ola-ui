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
    self._ss = SelectServer()
    self._ss.AddReadDescriptor(self._client.GetSocket(),
                               self._client.SocketReady)
    print 'Starting the OLA event loop'
    self._ss.Run()
    print 'OLA thread finished'
 
  def Stop(self):
    if self._ss is None:
      print 'OLAThread.Stop() called before thread was running'
      return
 
    print 'Stopping OLA thread'
    self._ss.Terminate()                                                                                                                                  
 
  def Execute(self, cb):
    print 'calling execute'
    self._ss.Execute(cb)
 
if __name__ == '__main__':
	print 'olathreading'
# 	def thread_fn(olathread):
# 		olathread._client.RunRDMDiscovery(1, True, upondiscover)
# 		print 'currently in thread: %d \n' % threading.currentThread().ident
# 
# 	def upondiscover(status, uids):
# 		print 'discovered'
# 		for uid in uids:
# 			print uid
# 
# 	ola_thread = OLAThread()
# 	ola_thread.start()
# 	print 'currently in thread: %d \n' % threading.currentThread().ident
# 	time.sleep(1)
#  
# 	print 'back from sleep'
# 	f = lambda : thread_fn(ola_thread)
# 	ola_thread.Execute(f)
# 	print 'back from sleep'
#  
# 	time.sleep(1)