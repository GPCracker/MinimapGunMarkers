package net.GPCracker.MinimapGunMarkers.entries
{
	import flash.display.Sprite;
	import flash.geom.ColorTransform;

	import net.GPCracker.Application;
	import net.GPCracker.base.AtlasSprite;
	import net.GPCracker.battle.views.components.minimap.entries.ScalableMinimapEntry;

	public class VehicleGunMinimapEntry extends ScalableMinimapEntry
	{
		public var gunDirection:AtlasSprite = null;

		public function VehicleGunMinimapEntry()
		{
			super();
			this.gunDirection = new AtlasSprite(Application.atlasManager);
			this.addChild(this.gunDirection);
			return;
		}

		private function setGraphics(source:String, offsetX:Number=0.0, offsetY:Number=0.0, smooth:Boolean=false, repeat:Boolean=false, center:Boolean=false):void
		{
			this.gunDirection.x = offsetX;
			this.gunDirection.y = offsetY;
			this.gunDirection.fillSmooth = smooth;
			this.gunDirection.fillRepeat = repeat;
			this.gunDirection.fillCenter = center;
			// Changing source will cause auto redraw.
			this.gunDirection.source = source;
			return;
		}

		public function as_setGraphics(...args):void
		{
			if (1 <= args.length && args.length <= 6)
			{
				var source:String = args.shift();
				var offsetX:Number = args.length ? args.shift() : 0.0;
				var offsetY:Number = args.length ? args.shift() : 0.0;
				var smooth:Boolean = args.length ? args.shift() : false;
				var repeat:Boolean = args.length ? args.shift() : false;
				var center:Boolean = args.length ? args.shift() : false;
				this.setGraphics(source, offsetX, offsetY, smooth, repeat, center);
			}
			else
			{
				throw new ArgumentError("Error #1063: Argument count mismatch.");
			}
			return;
		}
	}
}
