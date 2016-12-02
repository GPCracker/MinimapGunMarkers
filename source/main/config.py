# *************************
# Configuration
# *************************
_config_ = None

# *************************
# Default configuration
# *************************
def defaultConfig():
	return {
		'applicationEnabled': ('Bool', True),
		'ignoreClientVersion': ('Bool', True),
		'appLoadedMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#008000">successfully loaded.</font>'),
		'appFailedMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#E00000">is incompatible with current client version.</font>'),
		'vehicleGunMarkers': {
			'enabled': ('Bool', True),
			'activated': ('Bool', True),
			'shortcut': {
				'key': ('String', 'KEY_NONE'),
				'switch': ('Bool', True),
				'invert': ('Bool', False),
			},
			'message': {
				'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: GLOBAL ENABLED.'),
				'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: GLOBAL DISABLED.')
			},
			'filters': {
				'spg': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': {
						'key': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: SPG ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: SPG DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/ally'),
						'offset': ('Vector2AsTuple', (-35.0, -76.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: not gunEntry.isEnemy() and not gunEntry.isSquadMan() and gunEntry.getClassTag() in ('SPG', ))
				},
				'squad': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': {
						'key': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: SQUAD ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: SQUAD DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/squadman'),
						'offset': ('Vector2AsTuple', (-35.0, -76.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: not gunEntry.isEnemy() and gunEntry.isSquadMan())
				},
				'enemy': {
					'enabled': ('Bool', False),
					'activated': ('Bool', True),
					'shortcut': {
						'key': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					},
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: ENEMY ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: ENEMY DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/enemy'),
						'offset': ('Vector2AsTuple', (-35.0, -76.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: gunEntry.isEnemy())
				}
			}
		}
	}

# *************************
# Read configuration from file
# *************************
def readConfig():
	configReader = XModLib.XMLConfigReader.XMLConfigReader((
		('Vector2AsTuple', XModLib.XMLConfigReader.VectorAsTupleXMLReaderMeta.construct(
			'Vector2AsTupleXMLReader',
			vector_type='Vector2'
		)),
		('LocalizedWideString', XModLib.XMLConfigReader.LocalizedWideStringXMLReaderMeta.construct(
			'LocalizedWideStringXMLReader',
			translator=_globals_['i18nFormatter']
		))
	))
	mainSection = configReader.open_section(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config file is missing. Loading defaults.'.format(__application__[1])
	else:
		print '[{}] Config file was found. Trying to load it.'.format(__application__[1])
	return configReader(mainSection, defaultConfig())
