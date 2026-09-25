"""Create a simple typographic sharing card in the site's colours."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
canvas = Image.new('RGB', (1200, 630), '#f5f2eb')
draw = ImageDraw.Draw(canvas)
fonts = Path('C:/Windows/Fonts')
serif = ImageFont.truetype(str(fonts/'georgia.ttf'), 76)
role = ImageFont.truetype(str(fonts/'georgia.ttf'), 38)
body = ImageFont.truetype(str(fonts/'segoeui.ttf'), 25)
small = ImageFont.truetype(str(fonts/'segoeui.ttf'), 21)
draw.rectangle((40, 40, 1160, 590), outline='#d4d8cc', width=2)
draw.text((85,85), 'PORTFOLIO', font=small, fill='#62685f')
draw.text((82,168), 'Salman Haider', font=serif, fill='#28372f')
draw.text((85,273), 'GIS Professional in Canada', font=role, fill='#365b49')
draw.line((85,374,1115,374), fill='#d4d8cc', width=2)
draw.text((85,414), 'Spatial analysis   ·   Python automation   ·   Cartography', font=body, fill='#62685f')
draw.text((85,516), 'salmanhaider.pro', font=small, fill='#365b49')
canvas.save(ROOT/'assets/images/social/portfolio-preview.png', optimize=True)
