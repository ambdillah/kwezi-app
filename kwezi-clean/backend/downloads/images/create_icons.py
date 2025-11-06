from PIL import Image, ImageDraw, ImageFont
import os

# Couleur principale de l'app
color = (102, 126, 234)  # #667eea

# Créer icon.png (1024x1024)
icon = Image.new('RGB', (1024, 1024), color)
draw = ImageDraw.Draw(icon)

# Dessiner un "K" stylisé au centre
draw.ellipse([200, 200, 824, 824], fill='white')
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 400)
except:
    font = ImageFont.load_default()
draw.text((512, 512), "K", fill=color, font=font, anchor="mm")

icon.save('icon.png')
print("✓ icon.png créé")

# Créer adaptive-icon.png (1024x1024)
adaptive_icon = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
draw = ImageDraw.Draw(adaptive_icon)

# Dessiner un cercle blanc avec "K"
draw.ellipse([100, 100, 924, 924], fill='white')
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 450)
except:
    font = ImageFont.load_default()
draw.text((512, 512), "K", fill=color, font=font, anchor="mm")

adaptive_icon.save('adaptive-icon.png')
print("✓ adaptive-icon.png créé")
