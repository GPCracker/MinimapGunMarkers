# --------------------------------------- #
#    VehicleGunMinimapGraphics Classes    #
# --------------------------------------- #
class GunEntryGraphics(collections.namedtuple('GunEntryGraphics', ('source', 'scale', 'offset', 'smooth', 'repeat', 'center'))):
	__slots__ = ()

	def __new__(cls, source, scale=(1.0, 1.0), offset=(0.0, 0.0), smooth=False, repeat=False, center=False):
		return super(GunEntryGraphics, cls).__new__(cls, source, scale, offset, smooth, repeat, center)

	def tuple(self):
		return (self.source, ) + self.scale + self.offset + (self.smooth, self.repeat, self.center)

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
		return hash((self._idx, ))

	def __eq__(self, other):
		if not isinstance(other, GunEntryFilter):
			return NotImplemented
		return self._idx == other.idx

	def __ne__(self, other):
		if not isinstance(other, GunEntryFilter):
			return NotImplemented
		return self._idx != other.idx

	def __repr__(self):
		return '{!s}(idx={!r}, graphics={!r}, function={!r})'.format(
			self.__class__.__name__,
			self._idx, self._graphics, self._function
		)

class GunEntryFilterCollection(frozenset):
	__slots__ = ('activated', )

	def __new__(cls, filters, *args, **kwargs):
		return super(GunEntryFilterCollection, cls).__new__(cls, filters)

	def __init__(self, filters, activated=True):
		super(GunEntryFilterCollection, self).__init__(filters)
		self.activated = activated
		return

	def _getFilter(self, idx):
		for efilter in self:
			if idx == efilter.idx:
				return efilter
		raise KeyError(idx)
		return

	def _getGraphics(self, gunEntry):
		generator = (efilter.graphics for efilter in self if efilter(gunEntry))
		graphics = next(generator, None)
		if graphics is not None and next(generator, None) is not None:
			raise RuntimeError('any entry must fit only one filter because entry graphics must be uniquely defined')
		return graphics

	def toggleGlobal(self, value):
		if value != self.activated:
			self.activated = value
			return True
		return False

	def toggleFilter(self, idx, value):
		efilter = self._getFilter(idx)
		if value != efilter.activated:
			efilter.activated = value
			return True
		return False

	def __call__(self, gunEntry):
		return self._getGraphics(gunEntry) if self.activated else None

	def __repr__(self):
		return frozenset.__repr__(self)

class GunEntryEvent(gui.shared.events.GameEvent):
	KEYBOARD_TOGGLE_GLOBAL = 'game/MinimapGunMarkers/keyboardToggleGlobal'
	KEYBOARD_TOGGLE_FILTER = 'game/MinimapGunMarkers/keyboardToggleFilter'
