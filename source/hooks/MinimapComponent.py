# *************************
# MinimapComponent Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, '_setupPlugins', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_MinimapComponent_setupPlugins(old_MinimapComponent_setupPlugins, self, *args, **kwargs):
	result = old_MinimapComponent_setupPlugins(self, *args, **kwargs)
	config = _config_['modules']['vehicleGunMarkers']
	if config['enabled']:
		def iterfilters(fcis):
			for idx, fconfig in fcis:
				if fconfig['enabled']:
					yield GunEntryFilter(idx, GunEntryGraphics(**fconfig['graphics']), fconfig['function'], fconfig['activated'])
			return
		result['guns'] = VehicleGunMinimapPlugin.factory(
			name='VehicleGunMinimapPlugin',
			filters=GunEntryFilterCollection(
				filters=iterfilters(config['filters'].iteritems()),
				activated=config['activated']
			)
		)
	return result

@XModLib.HookUtils.methodAddExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, 'as_createEntryContainerS')
def new_MinimapComponent_createEntryContainer(self, entryContainerName, entryContainerIndex):
	if self._isDAAPIInited():
		return self.flashObject.entriesContainer.as_createEntryContainer(entryContainerName, entryContainerIndex)
	return

@XModLib.HookUtils.methodHookExt(_inject_hooks_, gui.Scaleform.daapi.view.battle.shared.minimap.component.MinimapComponent, '_MinimapComponent__createComponent', invoke=XModLib.HookUtils.HookInvoke.SECONDARY)
def new_MinimapComponent_createComponent(self, *args, **kwargs):
	self.as_createEntryContainerS('guns', 5)
	return
