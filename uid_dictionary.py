# Victoria Tisdale
# uid_dictionary.py
# created: June 20, 2013

class UID_Dictionary:
	def __init__(self, uidList):
		self._UIDDict = {}
		self._UIDList = uidList
		for uid in uidList:
			self._UIDDict[uid] = {}
	
	def set(self, uid, key, value):
		if uid in self._UIDList:
			self._uid_dict[uid][key] = value
		# should this return something so that I can check weather or not it worked
	
	def get(self, uid, key):
		if uid in self._UIDList:
			return self._UIDDict[uid][key]
			
	def getUIDs(self):
		return self._UIDDict.keys()