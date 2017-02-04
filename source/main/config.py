# *************************
# Application configuration
# *************************
def loadConfiguration():
	configReader = XModLib.XMLConfigReader.XMLConfigReader((
		('SimpleShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'SimpleShortcutXMLReader',
			constructor=lambda shortcut, **kwargs: XModLib.KeyboardUtils.Shortcut(shortcut, **kwargs),
			section_type='String'
		)),
		('AdvancedShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
			'AdvancedShortcutXMLReader',
			constructor=lambda shortcut: XModLib.KeyboardUtils.Shortcut(**shortcut),
			section_type='Dict'
		)),
		('Vector2AsTuple', XModLib.XMLConfigReader.VectorAsTupleXMLReaderMeta.construct(
			'Vector2AsTupleXMLReader',
			vector_type='Vector2'
		)),
		('LocalizedWideString', XModLib.XMLConfigReader.LocalizedWideStringXMLReaderMeta.construct(
			'LocalizedWideStringXMLReader',
			translator=_globals_['i18nFormatter']
		))
	))
	defaultConfig = {
		'applicationEnabled': ('Bool', True),
		'ignoreClientVersion': ('Bool', True),
		'appLoadedMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#008000">successfully loaded.</font>'),
		'appFailedMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#E00000">is incompatible with current client version.</font>'),
		'vehicleGunMarkers': {
			'enabled': ('Bool', True),
			'activated': ('Bool', True),
			'shortcut': ('AdvancedShortcut', {
				'sequence': ('String', 'KEY_NONE'),
				'switch': ('Bool', True),
				'invert': ('Bool', False),
			}),
			'message': {
				'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: GLOBAL ENABLED.'),
				'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: GLOBAL DISABLED.')
			},
			'filters': {
				'spg': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: SPG ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: SPG DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/ally'),
						'scale': ('Vector2AsTuple', (0.75, 0.75)),
						'offset': ('Vector2AsTuple', (-26.0, -58.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: not gunEntry.isEnemy() and not gunEntry.isSquadMan() and gunEntry.getClassTag() in ('SPG', ))
				},
				'squad': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: SQUAD ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: SQUAD DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/squadman'),
						'scale': ('Vector2AsTuple', (0.75, 0.75)),
						'offset': ('Vector2AsTuple', (-26.0, -58.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: not gunEntry.isEnemy() and gunEntry.isSquadMan())
				},
				'enemy': {
					'enabled': ('Bool', False),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False),
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'MinimapGunMarkers: ENEMY ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'MinimapGunMarkers: ENEMY DISABLED.')
					},
					'graphics': {
						'source': ('String', 'MinimapGunMarkers:markers/enemy'),
						'scale': ('Vector2AsTuple', (0.75, 0.75)),
						'offset': ('Vector2AsTuple', (-26.0, -58.0)),
						'smooth': ('Bool', True)
					},
					'function': ('Internal', lambda gunEntry: gunEntry.isEnemy())
				}
			}
		}
	}
	mainSection = configReader.open_section(os.path.splitext(__file__)[0] + '.xml')
	if mainSection is None:
		print '[{}] Config file is missing. Loading defaults.'.format(__application__[1])
	else:
		print '[{}] Config file was found. Trying to load it.'.format(__application__[1])
	return configReader(mainSection, defaultConfig)

# *************************
# Configuration init
# *************************
_config_ = loadConfiguration()
