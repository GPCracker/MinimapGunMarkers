# ------------ #
#    Python    #
# ------------ #
import os
import sys
import math
import time
import marshal
import weakref
import zipfile
import functools
import collections

# -------------- #
#    BigWorld    #
# -------------- #
import Math
import BigWorld

# ---------------- #
#    WoT Client    #
# ---------------- #
import constants
import PlayerEvents
import gui.shared.personality

# -------------------- #
#    WoT Client GUI    #
# -------------------- #
import gui.shared
import gui.shared.events
import gui.battle_control.arena_info.interfaces
import gui.Scaleform.daapi.view.battle.shared.minimap.common
import gui.Scaleform.daapi.view.battle.shared.minimap.entries

# ---------------------- #
#    WoT Client Hooks    #
# ---------------------- #
import Account
import AvatarInputHandler

# -------------------------- #
#    WoT Client GUI Hooks    #
# -------------------------- #
import gui.Scaleform.battle_entry
import gui.Scaleform.daapi.view.battle.shared.minimap.component

# ------------------- #
#    X-Mod Library    #
# ------------------- #
import XModLib.HookUtils
import XModLib.MathUtils
import XModLib.TextUtils
import XModLib.ClientUtils
import XModLib.EngineUtils
import XModLib.CallbackUtils
import XModLib.KeyboardUtils
import XModLib.ClientMessages
import XModLib.XMLConfigReader

# ----------------------- #
#    X-Mod GUI Library    #
# ----------------------- #
import XModLib.pygui.battle.library
