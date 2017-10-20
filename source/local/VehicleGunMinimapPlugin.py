# *************************
# VehicleGunMinimapPlugin Class
# *************************
class VehicleGunMinimapPlugin(gui.Scaleform.daapi.view.battle.shared.minimap.common.EntriesPlugin, gui.battle_control.arena_info.interfaces.IArenaVehiclesController):
	__slots__ = ('_filters', )

	symbol = 'net.GPCracker.MinimapGunMarkers.entries::VehicleGunMinimapEntry'
	container = 'guns'

	@classmethod
	def factory(cls, name, filters=frozenset(), activated=True):
		# This class method creates new subclass, that have specified filters collection.
		return type(name, (cls, ), {'_class_filters': filters, '_class_activated': activated})

	@staticmethod
	def getGunMatrixProvider(vehicleID):
		vehicle = BigWorld.entity(vehicleID)
		return XModLib.MathUtils.getCombinedMatrixProvider(
			vehicle.matrix,
			XModLib.MathUtils.getMatrixProduct(
				vehicle.appearance.gunMatrix,
				XModLib.MathUtils.getMatrixProduct(
					vehicle.appearance.turretMatrix,
					vehicle.matrix
				)
			)
		) if vehicle is not None else None

	def __init__(self, parent):
		super(VehicleGunMinimapPlugin, self).__init__(parent, clazz=VehicleGunMinimapEntry)
		self._filters = GunEntryFilterCollection(self._class_filters, self._class_activated)
		return

	@property
	def filters(self):
		return self._filters

	def start(self):
		super(VehicleGunMinimapPlugin, self).start()
		ctrl = self.sessionProvider.shared.feedback
		if ctrl is not None:
			ctrl.onMinimapVehicleAdded += self.__onMinimapVehicleAdded
			ctrl.onMinimapVehicleRemoved += self.__onMinimapVehicleRemoved
		PlayerEvents.g_playerEvents.onTeamChanged += self.__onTeamChanged
		self.sessionProvider.addArenaCtrl(self)
		gui.shared.g_eventBus.addListener(GunEntryEvent.KEYBOARD_TOGGLE_GLOBAL, self.__handleToggleGlobal, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		gui.shared.g_eventBus.addListener(GunEntryEvent.KEYBOARD_TOGGLE_FILTER, self.__handleToggleFilter, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		return

	def stop(self):
		gui.shared.g_eventBus.removeListener(GunEntryEvent.KEYBOARD_TOGGLE_GLOBAL, self.__handleToggleGlobal, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		gui.shared.g_eventBus.removeListener(GunEntryEvent.KEYBOARD_TOGGLE_FILTER, self.__handleToggleFilter, gui.shared.EVENT_BUS_SCOPE.BATTLE)
		self.sessionProvider.removeArenaCtrl(self)
		ctrl = self.sessionProvider.shared.feedback
		if ctrl is not None:
			ctrl.onMinimapVehicleAdded -= self.__onMinimapVehicleAdded
			ctrl.onMinimapVehicleRemoved -= self.__onMinimapVehicleRemoved
		PlayerEvents.g_playerEvents.onTeamChanged -= self.__onTeamChanged
		super(VehicleGunMinimapPlugin, self).stop()
		return

	def __addEntry(self, vehicleID):
		matrix = self.getGunMatrixProvider(vehicleID)
		active = matrix is not None
		entry = self._addEntryEx(vehicleID, self.symbol, self.container, matrix=matrix, active=active)
		if entry is not None:
			entry.setPlugin(self)
		return entry

	def __initEntry(self, entry, vInfo):
		vehicleID = vInfo.vehicleID
		entry.init(
			isCtrl=self.__isCtrl(vehicleID),
			isAlive=vInfo.isAlive(),
			isEnemy=self._arenaDP.isEnemyTeam(vInfo.team),
			classTag=vInfo.vehicleType.classTag,
			isPlayer=self.__isPlayer(vehicleID),
			isSquadMan=self._arenaDP.isSquadMan(vehicleID),
			isTeamKiller=vInfo.isTeamKiller()
		)
		entry.updateGraphics()
		return

	def __updateEntry(self, entry, vInfo):
		vehicleID = vInfo.vehicleID
		entry.update(
			isAlive=vInfo.isAlive(),
			isEnemy=self._arenaDP.isEnemyTeam(vInfo.team),
			classTag=vInfo.vehicleType.classTag,
			isPlayer=self.__isPlayer(vehicleID),
			isSquadMan=self._arenaDP.isSquadMan(vehicleID),
			isTeamKiller=vInfo.isTeamKiller()
		)
		entry.updateGraphics()
		return

	def __delEntry(self, vehicleID):
		return self._delEntryEx(vehicleID)

	def __isCtrl(self, vehicleID):
		if self._isInPostmortemMode() or self._isInVideoMode():
			return self._ctrlVehicleID == vehicleID
		return self._arenaDP.getPlayerVehicleID() == vehicleID

	def __isPlayer(self, vehicleID):
		return self._arenaDP.getPlayerVehicleID() == vehicleID

	def __onMinimapVehicleAdded(self, vProxy, vInfo, guiProps):
		if vInfo.isObserver():
			return
		vehicleID = vInfo.vehicleID
		if vehicleID in self._entries:
			entry = self._entries[vehicleID]
			entry.setMatrix(self.getGunMatrixProvider(vehicleID))
			entry.updateGraphics()
			return
		entry = self.__addEntry(vehicleID)
		if entry is not None:
			self.__initEntry(entry, vInfo)
		return

	def __onMinimapVehicleRemoved(self, vehicleID):
		if vehicleID in self._entries:
			entry = self._entries[vehicleID]
			entry.setMatrix(None)
			entry.updateGraphics()
		return

	def __onTeamChanged(self, team):
		self.invalidateArenaInfo()
		return

	def __handleToggleGlobal(self, event):
		ctx = event.ctx
		if self._filters.toggleGlobal(ctx['activated']):
			self.updateEntriesGraphics()
		return

	def __handleToggleFilter(self, event):
		ctx = event.ctx
		if self._filters.toggleFilter(ctx['idx'], ctx['activated']):
			self.updateEntriesGraphics()
		return

	def updateEntriesGraphics(self):
		for vehicleID in self._entries:
			entry = self._entries[vehicleID]
			entry.updateGraphics()
		return

	def updateControlMode(self, mode, vehicleID):
		prevCtrlVehicleID = self._ctrlVehicleID
		super(VehicleGunMinimapPlugin, self).updateControlMode(mode, vehicleID)
		currCtrlVehicleID = self._ctrlVehicleID
		if prevCtrlVehicleID and prevCtrlVehicleID in self._entries:
			entry = self._entries[prevCtrlVehicleID]
			entry.setCtrl(False)
			entry.updateGraphics()
		if currCtrlVehicleID and currCtrlVehicleID in self._entries:
			entry = self._entries[currCtrlVehicleID]
			entry.setCtrl(True)
			entry.updateGraphics()
		return

	def spaceLoadStarted(self):
		"""Arena space loading started."""
		return

	def spaceLoadCompleted(self):
		"""Arena space loading completed."""
		return

	def updateSpaceLoadProgress(self, progress):
		"""Arena space loading progress has been changed
		:param progress: [float] progress value
		"""
		return

	def arenaLoadCompleted(self):
		"""Arena space loading completed and influx draw enabled. This event
		means arena is ready to be shown.
		"""
		return

	def invalidateArenaInfo(self):
		"""Starts to invalidate information of arena."""
		self.invalidateVehiclesInfo(self._arenaDP)
		return

	def invalidateVehiclesInfo(self, arenaDP):
		"""New list of vehicles has been received.
		:param arenaDP: instance of ArenaDataProvider.
		"""
		for vehicleID in self._entries:
			self.__delEntry(vehicleID)
		for vInfo in arenaDP.getVehiclesInfoIterator():
			if vInfo.isObserver():
				continue
			vehicleID = vInfo.vehicleID
			entry = self.__addEntry(vehicleID)
			if entry is not None:
				self.__initEntry(entry, vInfo)
		return

	def addVehicleInfo(self, vInfo, arenaDP):
		"""New vehicle added to arena.
		:param vo: instance of VehicleArenaInfoVO that has been added.
		:param arenaDP: instance of ArenaDataProvider.
		"""
		vehicleID = vInfo.vehicleID
		if vInfo.isObserver() or vehicleID in self._entries:
			return
		entry = self.__addEntry(vehicleID)
		if entry is not None:
			self.__initEntry(entry, vInfo)
		return

	def updateVehiclesInfo(self, updated, arenaDP):
		"""Vehicle has been updated on arena.
        :param updated: container of VOs which have been changed, where first element belongs to updated vehicle
        :param arenaDP: instance of ArenaDataProvider.
        """
		for flags, vInfo in updated:
			vehicleID = vInfo.vehicleID
			if vInfo.isObserver() or vehicleID not in self._entries:
				continue
			entry = self._entries[vehicleID]
			self.__updateEntry(entry, vInfo)
		return

	def invalidateVehicleStatus(self, flags, vInfo, arenaDP):
		"""Status of vehicle (isReady, isAlive, ...) has been updated on arena.
		:param flags: bitmask containing values from INVALIDATE_OP.
		:param vInfo: instance of VehicleArenaInfoVO for that status is updated.
		:param arenaDP: instance of ArenaDataProvider.
		"""
		if vInfo.isObserver():
			return
		vehicleID = vInfo.vehicleID
		if vehicleID in self._entries:
			entry = self._entries[vehicleID]
			entry.setAlive(vInfo.isAlive())
			entry.updateGraphics()
		return

	def invalidatePlayerStatus(self, flags, vInfo, arenaDP):
		"""Status of player (isTeamKiller, ...) has been updated on arena.
		:param flags: bitmask containing values from INVALIDATE_OP.
		:param vInfo: instance of VehicleArenaInfoVO for that status updated.
		:param arenaDP: instance of ArenaDataProvider.
		"""
		if vInfo.isObserver():
			return
		vehicleID = vInfo.vehicleID
		if vehicleID in self._entries:
			entry = self._entries[vehicleID]
			entry.setSquadMan(self._arenaDP.isSquadMan(vehicleID))
			entry.setTeamKiller(vInfo.isTeamKiller())
			entry.updateGraphics()
		return
