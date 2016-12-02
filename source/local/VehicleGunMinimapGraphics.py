# *************************
# VehicleGunMinimap Classes
# *************************
class GunEntryGraphics(collections.namedtuple('GunEntryGraphics', ('source', 'offset', 'smooth', 'repeat', 'center'))):
	__slots__ = ()

	def __new__(sclass, source, offset=(0.0, 0.0), smooth=False, repeat=False, center=False):
		return super(GunEntryGraphics, sclass).__new__(sclass, source, offset, smooth, repeat, center)

	def tuple(self):
		return (self.source, ) + self.offset + (self.smooth, self.repeat, self.center)

class GunEntryFilter(object):
	__slots__ = ('_idx', '_graphics', '_function', 'activated')

	DEFAULT_GRAPHICS = GunEntryGraphics(None)
	DEFAULT_FUNCTION = lambda gunEntry: False

	def __init__(self, idx, graphics=None, function=None, activated=True):
		super(GunEntryFilter, self).__init__()
		self._idx = idx
		self._graphics = graphics if graphics is not None else self.DEFAULT_GRAPHICS
		self._function = function if function is not None else self.DEFAULT_FUNCTION
		self.activated = activated
		return

	@property
	def idx(self):
		return self._idx

	@property
	def graphics(self):
		return self._graphics

	@property
	def function(self):
		return self._function

	def __call__(self, gunEntry):
		return self.activated and self._function(gunEntry)

	def __hash__(self):
		return hash(self._idx)

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return self._idx == other.idx and self._graphics == other.graphics and self._function == other.function

	def __repr__(self):
		return '{}(idx={!r}, graphics={!r}, function={!r})'.format(self.__class__.__name__, self._idx, self._graphics, self._function)

class GunEntryFilterCollection(frozenset):
	__slots__ = ('_activated', )

	def __init__(self, filters, activated=True):
		super(GunEntryFilterCollection, self).__init__(filters)
		self._activated = activated
		return

	def __new__(sclass, filters, activated=True):
		return super(GunEntryFilterCollection, sclass).__new__(sclass, filters)

	@property
	def activated(self):
		return self._activated

	def _getFilter(self, idx):
		efilter = next((efilter for efilter in self if idx == efilter.idx), None)
		if efilter is None:
			raise KeyError('GunEntryFilter with an appropriate identifier does not exist.')
		return efilter

	def _getGraphics(self, gunEntry):
		graphics = [efilter.graphics for efilter in self if efilter(gunEntry)]
		if len(graphics) > 1:
			raise RuntimeError('Any entry should fit only one filter, otherwise entry graphics could not be definitely chosen.')
		return graphics.pop() if graphics else None

	def toggleGlobal(self, value):
		if value != self._activated:
			self._activated = value
			return True
		return False

	def toggleFilter(self, idx, value):
		efilter = self._getFilter(idx)
		if value != efilter.activated:
			efilter.activated = value
			return True
		return False

	def __call__(self, gunEntry):
		return self._getGraphics(gunEntry) if self._activated else None

	def __repr__(self):
		return super(GunEntryFilterCollection, self).__repr__()

class GunEntryEvent(gui.shared.events.GameEvent):
	KEYBOARD_TOGGLE_GLOBAL = 'game/MinimapGunMarkers/keyboardToggleGlobal'
	KEYBOARD_TOGGLE_FILTER = 'game/MinimapGunMarkers/keyboardToggleFilter'
