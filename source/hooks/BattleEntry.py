# *************************
# BattleEntry Hooks
# *************************
@XModLib.HookUtils.methodHookExt(_inject_hooks_, gui.Scaleform.battle_entry.BattleEntry, '_getRequiredLibraries', invoke=XModLib.HookUtils.HookInvoke.MASTER)
def new_BattleEntry_getRequiredLibraries(old_BattleEntry_getRequiredLibraries, self, *args, **kwargs):
	return old_BattleEntry_getRequiredLibraries(self, *args, **kwargs) + ('MinimapGunMarkers.swf', )
