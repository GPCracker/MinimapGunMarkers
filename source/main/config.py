# -------------------------------------- #
#    Application configuration reader    #
# -------------------------------------- #
g_globals['appConfigReader'] = XModLib.XMLConfigReader.XMLConfigReader((
	('SimpleShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
		'SimpleShortcutXMLReader',
		constructor=lambda shortcut, **kwargs: XModLib.KeyboardUtils.Shortcut(shortcut, **kwargs),
		sectionType='String'
	)),
	('AdvancedShortcut', XModLib.XMLConfigReader.DataObjectXMLReaderMeta.construct(
		'AdvancedShortcutXMLReader',
		constructor=lambda shortcut: XModLib.KeyboardUtils.Shortcut(**shortcut),
		sectionType='Dict'
	))
))

# --------------------------------------- #
#    Application default configuration    #
# --------------------------------------- #
g_globals['appDefaultConfig'] = {
	'applicationEnabled': ('Bool', True),
	'ignoreClientVersion': ('Bool', False),
	'appSuccessMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#008000">was successfully loaded.</font>'),
	'appWarningMessage': ('LocalizedWideString', u'<a href="event:MinimapGunMarkers.official_topic"><font color="#0080FF">"Minimap&nbsp;Gun&nbsp;Markers"</font></a> <font color="#E00000">was not tested with current client version.</font>'),
	'modules': {
		'vehicleGunMarkers': {
			'enabled': ('Bool', True),
			'activated': ('Bool', True),
			'shortcut': ('AdvancedShortcut', {
				'sequence': ('String', 'KEY_NONE'),
				'switch': ('Bool', True),
				'invert': ('Bool', False)
			}),
			'message': {
				'onActivate': ('LocalizedWideString', u'[MinimapGunMarkers] GLOBAL ENABLED.'),
				'onDeactivate': ('LocalizedWideString', u'[MinimapGunMarkers] GLOBAL DISABLED.')
			},
			'filters': {
				'spg': {
					'enabled': ('Bool', True),
					'activated': ('Bool', True),
					'shortcut': ('AdvancedShortcut', {
						'sequence': ('String', 'KEY_NONE'),
						'switch': ('Bool', True),
						'invert': ('Bool', False)
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'[MinimapGunMarkers] SPG ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'[MinimapGunMarkers] SPG DISABLED.')
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
						'invert': ('Bool', False)
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'[MinimapGunMarkers] SQUAD ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'[MinimapGunMarkers] SQUAD DISABLED.')
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
						'invert': ('Bool', False)
					}),
					'message': {
						'onActivate': ('LocalizedWideString', u'[MinimapGunMarkers] ENEMY ENABLED.'),
						'onDeactivate': ('LocalizedWideString', u'[MinimapGunMarkers] ENEMY DISABLED.')
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
	},
	'plugins': {},
	'gui': {}
}

# ----------------------------------------- #
#    Application configuration root file    #
# ----------------------------------------- #
g_globals['appConfigFile'] = os.path.splitext(__file__)[0] + '.xml'

# --------------------------------------------- #
#    Application configuration reading stage    #
# --------------------------------------------- #
g_config = g_globals['appConfigReader'](
	XModLib.XMLConfigReader.openSection(g_globals['appConfigFile']),
	g_globals['appDefaultConfig']
)
