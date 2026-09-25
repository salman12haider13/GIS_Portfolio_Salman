"""Create smaller display copies without cropping or changing map content."""
from pathlib import Path
import json
from xml.etree import ElementTree
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'assets/images/maps/display'
out.mkdir(parents=True, exist_ok=True)
sizes = {}
for path in sorted((ROOT / 'assets/images/maps/full').iterdir()):
    if path.suffix.lower() not in {'.jpg', '.png', '.jpeg'}:
        continue
    destination = out / (path.stem + '.webp')
    if destination.exists() and destination.stat().st_mtime >= path.stat().st_mtime:
        continue
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert('RGB')
        image.thumbnail((2200, 2800), Image.Resampling.LANCZOS)
        image.save(destination, 'WEBP', quality=90, method=6)
for path in (ROOT / 'assets/images').rglob('*'):
    if path.is_file() and path.suffix.lower() in {'.jpg', '.png', '.webp', '.jpeg'}:
        try:
            with Image.open(path) as image:
                sizes[path.relative_to(ROOT).as_posix()] = list(image.size)
        except OSError:
            pass
    elif path.is_file() and path.suffix.lower() == '.svg':
        viewbox = ElementTree.parse(path).getroot().get('viewBox', '').split()
        if len(viewbox) == 4:
            sizes[path.relative_to(ROOT).as_posix()] = [round(float(v) * 10) for v in viewbox[2:]]
(ROOT / 'content').mkdir(exist_ok=True)
(ROOT / 'content/image-sizes.json').write_text(json.dumps(sizes, indent=2), encoding='utf-8')
print(f'Prepared {len(list(out.glob("*.webp")))} complete map images.')
