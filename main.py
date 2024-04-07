from moviepy.editor import ImageSequenceClip
from PIL import Image, ImageDraw, ImageFont
import os

# Simulate basic syntax highlighting for Python code
def syntax_highlight(text):
    keywords = ["print", "def", "for", "in", "return", "if", "else"]
    colors = {"keyword": "blue", "string": "green", "default": "black"}
    
    highlighted_text = []
    words = text.split(" ")
    for word in words:
        color = colors["default"]
        if word in keywords:
            color = colors["keyword"]
        elif word.startswith("'") and word.endswith("'") or word.startswith('"') and word.endswith('"'):
            color = colors["string"]
        highlighted_text.append((word, color))
    return highlighted_text

# Your Python code as a string
code = "print('Hello, World!')"

# Font settings (Adjust the path to your font file)
font_path = "./fonts/ARLRDBD.ttf"  # Adjust this path to the font you want to use
font_size = 20
font = ImageFont.truetype(font_path, font_size)

# Image settings
img_width, img_height = 800, 100
background_color = "white"
rect_color = "lightgrey"  # Color for the rectangle container
padding = 10  # Padding around the rectangle

# Generate a sequence of images
images = []
for i in range(1, len(code) + 1):
    img = Image.new("RGB", (img_width, img_height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a rectangle container
    draw.rectangle([padding, padding, img_width - padding, img_height - padding], outline=rect_color, width=2)
    
    # Apply simplified syntax highlighting
    partial_code = syntax_highlight(code[:i])
    x, y = 20, 30  # Starting position for the text
    for word, color in partial_code:
        draw.text((x, y), word, fill=color, font=font)
        word_width = draw.textlength(word + " ", font=font)  # Correct method to get text size
        word_height = font_size
        x += word_width  # Move x for the next word

    images.append(img)

# Save images to a temporary directory
temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)
filenames = []
for idx, img in enumerate(images):
    filename = os.path.join(temp_dir, f"{idx}.png")
    img.save(filename)
    filenames.append(filename)

# Create a video clip from images
clip = ImageSequenceClip(filenames, fps=10)  # Adjust fps for typing speed

# Export the video
output_video = "typing_effect.mp4"
clip.write_videofile(output_video, codec="libx264")

# Cleanup: remove temporary images
for filename in filenames:
    os.remove(filename)
os.rmdir(temp_dir)

print(f"Video saved as {output_video}")
