# *************************
# VehicleGunMinimapEntry Class
# *************************
class VehicleGunMinimapEntry(gui.Scaleform.daapi.view.battle.shared.minimap.entries.MinimapEntry):
	__slots__ = (
		'_plugin', '_graphics',
		'_isCtrl', '_isAlive', '_isEnemy', '_classTag', '_isPlayer', '_isSquadMan', '_isTeamKiller'
	)

	def __init__(self, entryID, active, matrix=None):
		super(VehicleGunMinimapEntry, self).__init__(entryID, active, matrix)
		self._plugin = None
		self._graphics = None
		return

	def init(self, **kwargs):
		# Here is no default value. If value is missing, we will get an exception.
		self._isCtrl = kwargs['isCtrl']
		self._isAlive = kwargs['isAlive']
		self._isEnemy = kwargs['isEnemy']
		self._classTag = kwargs['classTag']
		self._isPlayer = kwargs['isPlayer']
		self._isSquadMan = kwargs['isSquadMan']
		self._isTeamKiller = kwargs['isTeamKiller']
		return

	def update(self, **kwargs):
		# Here is no default value. If value is missing, we will pass.
		if 'isCtrl' in kwargs: self._isCtrl = kwargs['isCtrl']
		if 'isAlive' in kwargs: self._isAlive = kwargs['isAlive']
		if 'isEnemy' in kwargs: self._isEnemy = kwargs['isEnemy']
		if 'classTag' in kwargs: self._classTag = kwargs['classTag']
		if 'isPlayer' in kwargs: self._isPlayer = kwargs['isPlayer']
		if 'isSquadMan' in kwargs: self._isSquadMan = kwargs['isSquadMan']
		if 'isTeamKiller' in kwargs: self._isTeamKiller = kwargs['isTeamKiller']
		return

	def isDisplayable(self):
		# This method is required to prevent displaying of bad markers.
		# At least all markers of invisible vehicles should be disabled.
		# Gun matrix could be calculated only for vehicles in AOI (spotted, in drawing area).
		return self.isVisible() and self.isAlive() and not self.isCtrl()

	def updateGraphics(self):
		# This method is called when entry graphics need to be updated.
		# It acquires graphics profile and sets it and visibility status.
		graphics = self._plugin.filters(self) if self.isDisplayable() else None
		if graphics is not None:
			self.setActive(True)
			self.setGraphics(graphics)
		else:
			self.setActive(False)
		return

	def getPlugin(self):
		return self._plugin

	def setPlugin(self, plugin):
		self._plugin = plugin
		return True

	def getGraphics(self):
		return self._graphics

	def setGraphics(self, graphics):
		if graphics != self._graphics:
			self._graphics = graphics
			self._plugin._invoke(self.getID(), 'as_setGraphics', *graphics.tuple())
			return True
		return False

	def setMatrix(self, matrix):
		result = super(VehicleGunMinimapEntry, self).setMatrix(matrix)
		if result:
			self._plugin._setMatrix(self.getID(), matrix)
		return result

	def setActive(self, active):
		result = super(VehicleGunMinimapEntry, self).setActive(active)
		if result:
			self._plugin._setActive(self.getID(), active)
		return result

	def isVisible(self):
		return self._matrix is not None

	def isCtrl(self):
		return self._isCtrl

	def setCtrl(self, isCtrl):
		if isCtrl != self._isCtrl:
			self._isCtrl = isCtrl
			return True
		return False

	def isAlive(self):
		return self._isAlive

	def setAlive(self, isAlive):
		if isAlive != self._isAlive:
			self._isAlive = isAlive
			return True
		return False

	def isEnemy(self):
		return self._isEnemy

	def setEnemy(self, isEnemy):
		if isEnemy != self._isEnemy:
			self._isEnemy = isEnemy
			return True
		return False

	def getClassTag(self):
		return self._classTag

	def setClassTag(self, classTag):
		if classTag != self._classTag:
			self._classTag = classTag
			return True
		return False

	def isPlayer(self):
		return self._isPlayer

	def setPlayer(self, isPlayer):
		if isPlayer != self._isPlayer:
			self._isPlayer = isPlayer
			return True
		return False

	def isSquadMan(self):
		return self._isSquadMan

	def setSquadMan(self, isSquadMan):
		if isSquadMan != self._isSquadMan:
			self._isSquadMan = isSquadMan
			return True
		return False

	def isTeamKiller(self):
		return self._isTeamKiller

	def setTeamKiller(self, isTeamKiller):
		if isTeamKiller != self._isTeamKiller:
			self._isTeamKiller = isTeamKiller
			return True
		return False

	def clear(self):
		self._plugin = None
		self._graphics = None
		super(VehicleGunMinimapEntry, self).clear()
		return
