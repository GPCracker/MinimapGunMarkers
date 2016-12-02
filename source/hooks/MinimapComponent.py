# *************************
# MinimapComponent Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, '_setupPlugins', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_MinimapComponent_setupPlugins(old_MinimapComponent_setupPlugins, self, *args, **kwargs):
	result = old_MinimapComponent_setupPlugins(self, *args, **kwargs)
	config = _config_['vehicleGunMarkers']
	if config['enabled']:
		efilter = lambda idx, graphics, function, activated: GunEntryFilter(idx, GunEntryGraphics(**graphics), function, activated)
		result['guns'] = VehicleGunMinimapPlugin.factory(
			'VehicleGunMinimapPlugin',
			[efilter(idx, fconfig['graphics'], fconfig['function'], fconfig['activated']) for idx, fconfig in config['filters'].iteritems() if fconfig['enabled']],
			config['activated']
		)
	return result

@XModLib.HookUtils.HookFunction.methodAddOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, 'as_createEntryContainerS')
def new_MinimapComponent_createEntryContainer(self, entryContainerName, entryContainerIndex):
	if self._isDAAPIInited():
		return self.flashObject.entriesContainer.as_createEntryContainer(entryContainerName, entryContainerIndex)
	return

@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, '_MinimapComponent__createComponent', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_BEFORE_HOOK)
def new_MinimapComponent_createComponent(self, *args, **kwargs):
	self.as_createEntryContainerS('guns', 5)
	return
