# *************************
# AvatarInputHandler Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent')
def new_AvatarInputHandler_handleKeyEvent(self, event):
	getShortcut = XModLib.KeyBoard.Shortcut.fromSequence
	## HotKeys - VehicleGunMarkers
	mconfig = _config_['vehicleGunMarkers']
	if mconfig['enabled']:
		## HotKeys - VehicleGunMarkers - Global
		fconfig = mconfig
		shortcutHandle = fconfig['enabled'] and getShortcut(
			fconfig['shortcut']['key'],
			fconfig['shortcut']['switch'],
			fconfig['shortcut']['invert']
		)(event)
		if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
			fconfig['activated'] = shortcutHandle(fconfig['activated'])
			if shortcutHandle.switch and fconfig['activated']:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					fconfig['message']['onActivate'],
					'green'
				)
			elif shortcutHandle.switch:
				XModLib.Messages.Messenger.showMessageOnPanel(
					'Player',
					None,
					fconfig['message']['onDeactivate'],
					'red'
				)
			gui.shared.g_eventBus.handleEvent(
				GunEntryEvent(GunEntryEvent.KEYBOARD_TOGGLE_GLOBAL, {'activated': fconfig['activated']}),
				scope=gui.shared.EVENT_BUS_SCOPE.BATTLE
			)
		## HotKeys - VehicleGunMarkers - Filters
		fconfig = mconfig['filters']
		for idx, xconfig in fconfig.iteritems():
			shortcutHandle = xconfig['enabled'] and getShortcut(
				xconfig['shortcut']['key'],
				xconfig['shortcut']['switch'],
				xconfig['shortcut']['invert']
			)(event)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				xconfig['activated'] = shortcutHandle(xconfig['activated'])
				if shortcutHandle.switch and xconfig['activated']:
					XModLib.Messages.Messenger.showMessageOnPanel(
						'Player',
						None,
						xconfig['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.Messages.Messenger.showMessageOnPanel(
						'Player',
						None,
						xconfig['message']['onDeactivate'],
						'red'
					)
				gui.shared.g_eventBus.handleEvent(
					GunEntryEvent(GunEntryEvent.KEYBOARD_TOGGLE_FILTER, {'idx': idx, 'activated': xconfig['activated']}),
					scope=gui.shared.EVENT_BUS_SCOPE.BATTLE
				)
	return
