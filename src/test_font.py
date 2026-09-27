from PIL import ImageFont

font_path = r"C:\Users\kokat\OneDrive\Desktop\synthetic-manuscript-generator\fonts\devanagari\NotoSansDevanagari-Regular.ttf.ttf"

font = ImageFont.truetype(
    font_path,
    42
)

print("FONT WORKS!")
print(font)