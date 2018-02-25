# ------------------------------ #
#    AvatarInputHandler Hooks    #
# ------------------------------ #
@XModLib.HookUtils.methodHookExt(_inject_hooks_, AvatarInputHandler.AvatarInputHandler, 'handleKeyEvent', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_AvatarInputHandler_handleKeyEvent(old_AvatarInputHandler_handleKeyEvent, self, event):
	result = old_AvatarInputHandler_handleKeyEvent(self, event)
	## Keyboard event parsing
	kbevent = XModLib.KeyboardUtils.KeyboardEvent(event)
	## AvatarInputHandler started, event not handled by game (for avatar switches)
	if self._AvatarInputHandler__isStarted and not result:
		## HotKeys - VehicleGunMarkers
		mconfig = _config_['modules']['vehicleGunMarkers']
		if mconfig['enabled']:
			## HotKeys - VehicleGunMarkers - Global
			fconfig = mconfig
			shortcutHandle = fconfig['enabled'] and fconfig['shortcut'](kbevent)
			if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
				fconfig['activated'] = shortcutHandle(fconfig['activated'])
				if shortcutHandle.switch and fconfig['activated']:
					XModLib.ClientMessages.showMessageOnPanel(
						'Player',
						None,
						fconfig['message']['onActivate'],
						'green'
					)
				elif shortcutHandle.switch:
					XModLib.ClientMessages.showMessageOnPanel(
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
				shortcutHandle = xconfig['enabled'] and xconfig['shortcut'](kbevent)
				if shortcutHandle and (not shortcutHandle.switch or shortcutHandle.pushed):
					xconfig['activated'] = shortcutHandle(xconfig['activated'])
					if shortcutHandle.switch and xconfig['activated']:
						XModLib.ClientMessages.showMessageOnPanel(
							'Player',
							None,
							xconfig['message']['onActivate'],
							'green'
						)
					elif shortcutHandle.switch:
						XModLib.ClientMessages.showMessageOnPanel(
							'Player',
							None,
							xconfig['message']['onDeactivate'],
							'red'
						)
					gui.shared.g_eventBus.handleEvent(
						GunEntryEvent(GunEntryEvent.KEYBOARD_TOGGLE_FILTER, {'idx': idx, 'activated': xconfig['activated']}),
						scope=gui.shared.EVENT_BUS_SCOPE.BATTLE
					)
	## AvatarInputHandler started (for avatar shortcuts)
	if self._AvatarInputHandler__isStarted:
		pass
	return result
