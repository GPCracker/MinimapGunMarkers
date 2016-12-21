package net.GPCracker.MinimapGunMarkers.entries
{
	import flash.geom.Matrix;
	import flash.display.Sprite;

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

		private function setGraphics(source:String, smooth:Boolean=false, repeat:Boolean=false, center:Boolean=false):void
		{
			this.gunDirection.fillSmooth = smooth;
			this.gunDirection.fillRepeat = repeat;
			this.gunDirection.fillCenter = center;
			// Changing source will cause auto redraw.
			this.gunDirection.source = source;
			return;
		}

		private function setTransform(scaleX:Number=1.0, scaleY:Number=1.0, offsetX:Number=0.0, offsetY:Number=0.0):void
		{
			var matrix:Matrix = new Matrix();
			matrix.scale(scaleX, scaleY);
			matrix.translate(offsetX, offsetY);
			this.gunDirection.transform.matrix = matrix;
			return;
		}

		public function as_setGraphics(...args):void
		{
			if (1 <= args.length && args.length <= 8)
			{
				var source:String = args.shift();
				var scaleX:Number = args.length ? args.shift() : 1.0;
				var scaleY:Number = args.length ? args.shift() : 1.0;
				var offsetX:Number = args.length ? args.shift() : 0.0;
				var offsetY:Number = args.length ? args.shift() : 0.0;
				var smooth:Boolean = args.length ? args.shift() : false;
				var repeat:Boolean = args.length ? args.shift() : false;
				var center:Boolean = args.length ? args.shift() : false;
				this.setGraphics(source, smooth, repeat, center);
				this.setTransform(scaleX, scaleY, offsetX, offsetY);
			}
			else
			{
				throw new ArgumentError("Error #1063: Argument count mismatch.");
			}
			return;
		}
	}
}
