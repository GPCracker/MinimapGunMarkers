package net.GPCracker.MinimapGunMarkers
{
	import flash.display.Sprite;
	import flash.display.MovieClip;
	import net.wg.gui.battle.views.minimap.containers.MinimapEntriesContainer;

	import net.GPCracker.battle.views.components.minimap.containers.MinimapEntryContainer;

	public class LibraryMain extends MovieClip
	{
		public function LibraryMain()
		{
			super();
			MinimapEntriesContainer.prototype['as_createEntryContainer'] = function(entryContainerName:String, entryContainerIndex:Number=-1):void
			{
				if (this.getChildByName(entryContainerName) as Sprite)
				{
					DebugUtils.LOG_DEBUG("EntryContainer with name " + entryContainerName + " already exists.");
				}
				else
				{
					this.constructor.prototype[entryContainerName] = null;
					this[entryContainerName] = new MinimapEntryContainer();
					this[entryContainerName].name = entryContainerName
					if (0 <= entryContainerIndex && entryContainerIndex < this.numChildren)
					{
						this.addChildAt(this[entryContainerName], entryContainerIndex);
					}
					else
					{
						this.addChild(this[entryContainerName]);
					}
				}
				return;
			};
			return;
		}
	}
}
