# *************************
# BattleEntry Hooks
# *************************
@XModLib.HookUtils.HookFunction.methodHookOnEvent(_inject_hooks_, gui.Scaleform.battle_entry.BattleEntry, '_getRequiredLibraries', calltype=XModLib.HookUtils.HookFunction.CALL_ORIGIN_INSIDE_HOOK)
def new_BattleEntry_getRequiredLibraries(old_BattleEntry_getRequiredLibraries, self, *args, **kwargs):
	return old_BattleEntry_getRequiredLibraries(self, *args, **kwargs) + ('MinimapGunMarkers.swf', )
