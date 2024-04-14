from moviepy.editor import ImageSequenceClip, VideoFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import re



def create_clip(video_name, images, fps=5, has_end_pause=False, last_frame_pause_per_second=2, save_video=False):
    # Convert PIL Images to numpy arrays
    image_arrays = [np.array(img) for img in images]

    # pause a little on the last frame
    if has_end_pause and images:
        last_image_array = np.array(images[-1])
        pause_frames = [last_image_array] * (last_frame_pause_per_second * fps)
        image_arrays.extend(pause_frames)
    
    # Create video clip from image arrays
    clip = ImageSequenceClip(image_arrays, fps=fps)

    # Export the video
    if save_video:
        clip.write_videofile(video_name, codec="libx264")

    print(f"{video_name} created!")
    return clip

def create_image_with_overlay(bg_path, overlay_path, frame_size=(1080, 1920), h_padding=50, v_padding=50, overlay_shift=0):
    """
    Loads a background image and an overlay image, combines them, and saves or displays the result.
    
    :param bg_path: Path to the background image.
    :param overlay_path: Path to the overlay image (code window).
    :param frame_size: Tuple (width, height) of the output frame.
    :param overlay_position: Tuple (x, y) where the top-left corner of the overlay will be placed.
    """
    # Load the background image and resize it to the frame size
    bg_image = Image.open(bg_path).convert("RGBA")
    bg_image = bg_image.resize(frame_size, Image.Resampling.LANCZOS)  # Resize to fit the frame size
    
    # Load the overlay image
    overlay_image = Image.open(overlay_path).convert("RGBA")

    # Calculate new size for the overlay image, maintaining aspect ratio
    original_width, original_height = overlay_image.size
    new_width = frame_size[0] - 2 * h_padding
    new_height = int(original_height * (new_width / original_width))

    # Resize the overlay image
    overlay_image = overlay_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Calculate the position to center the overlay within the frame
    overlay_position = (h_padding+overlay_shift,v_padding)

    # Paste the overlay image onto the background image at the specified position
    bg_image.paste(overlay_image, overlay_position, overlay_image)  # Use overlay_image as a mask for transparency

    # Save or display the combined image
    # bg_image.show()
    return bg_image


def preprocess_line(text):
      words = []

      pattern = r'(\(|\))'
      words = re.split(pattern, text)
      result = []
      for word in words:
            if "'" not in word and "\"" not in word:
                  if " " in word:
                        pattern = r'(\s+)'
                        temp = re.split(pattern, word)
                        result += temp
                  else:
                        result.append(word)
            else:
                  if word.startswith("f"):                                              
                        result += ["f", word[1:]]
                  else:
                        result.append(word)

      return result

# Simulate basic syntax highlighting for Python code
def syntax_highlight(text):
    keywords = ["print", "def", "for", "in", "return", "if", "else"]
    colors = {"keyword": "#416ad1", "string": "#38783c", "function":"#e7eba2", "default": "#e1e8e2"}
    
    highlighted_text = []
    words = preprocess_line(text)
    for idx, word in enumerate(words):
        color = colors["default"]
        if word in keywords:
            color = colors["keyword"]
        elif word == "(":
            color = colors["function"]
            highlighted_text[-1] = (highlighted_text[-1][0], colors["function"])
        elif word == ")":
            color = colors["function"]
        elif word.startswith("'") or word.startswith('"'):
            color = colors["string"]
        highlighted_text.append((word, color))
    return highlighted_text


def draw_rounded_rectangle(draw, xy, corner_radius, fill):
    """
    Draws a rounded rectangle with the specified fill color.

    :param draw: An ImageDraw instance.
    :param xy: The bounding box, as a (left, top, right, bottom)-tuple.
    :param corner_radius: Radius of the corners.
    :param fill: The fill color.
    """
    upper_left, upper_right, bottom_left, bottom_right = xy
    # Draw the center rectangle
    draw.rectangle([upper_left + corner_radius, upper_right, bottom_left - corner_radius, bottom_right], fill=fill)
    # Draw the four sides
    draw.rectangle([upper_left, upper_right + corner_radius, bottom_left, bottom_right - corner_radius], fill=fill)
    # Draw the four corners
    draw.pieslice([upper_left, upper_right, upper_left + corner_radius * 2, upper_right + corner_radius * 2], start=180, end=270, fill=fill)
    draw.pieslice([bottom_left - corner_radius * 2, upper_right, bottom_left, upper_right + corner_radius * 2], start=270, end=360, fill=fill)
    draw.pieslice([upper_left, bottom_right - corner_radius * 2, upper_left + corner_radius * 2, bottom_right], start=90, end=180, fill=fill)
    draw.pieslice([bottom_left - corner_radius * 2, bottom_right - corner_radius * 2, bottom_left, bottom_right], start=0, end=90, fill=fill)


def add_text_to_image(image_path, output_path, text, position, font_path, font_size=20, text_color=(255, 255, 255)):
    """
    Adds text to an image and saves the result.

    :param image_path: Path to the input image.
    :param output_path: Path to save the modified image.
    :param text: Text to add to the image.
    :param position: Tuple (x, y) where the text will be added.
    :param font_path: Path to the font file.
    :param font_size: Size of the font.
    :param text_color: Color of the text as a tuple (R, G, B).
    """
    # Load the image
    image = Image.open(image_path).convert("RGBA")

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Define the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Font file not found, using default font.")
        font = ImageFont.load_default()

    # Add text to the image
    draw.text(position, text, font=font, fill=text_color)

    # Save the result
    image.save(output_path)
    # image.show()

def create_code_window_animation(background_image_path, overlay_image_path, ):
    images = []
    w_size = 1080
    selected_padding = w_size + 50
    for idx in np.linspace(0, selected_padding, 100):
        img = create_image_with_overlay(background_image_path, overlay_image_path, overlay_shift=(-selected_padding + round(idx)))
        images.append(img)
    
    return images

def generate_code_typing_effect(code_lines, given_background, font_path, font_size, font, padding=50, line_height_ratio = 1.2):
    # Generate a sequence of images
    images = []
    y_init = 0 + padding * 3
    bkg_image = None
    for code_line in code_lines:
        for i in range(1, len(code_line) + 1):
            if bkg_image:
                img = bkg_image.copy()
            else:
                img = given_background.copy()
            draw = ImageDraw.Draw(img)
            
            # Apply simplified syntax highlighting
            partial_code = syntax_highlight(code_line[:i])       
            x = 20 + padding * 1.25
            for word, color in partial_code:
                draw.text((x, y_init), word, fill=color, font=font)
                word_width = draw.textlength(word + " ", font=font)  # Correct method to get text size
                x += word_width  # Move x for the next word
            images.append(img)
        y_init += font_size * line_height_ratio
        bkg_image = img.copy()
    
    return images

def generate_choices_animation(background_image,  choices, v_padding = 700, v_padding_step = 120, num_frames = 50):
    background_image.save("question_done.png")
    images = []
    w_size = 1080
    selected_padding = w_size + 50
    for choice_idx, choice in enumerate(choices):
        for idx in np.linspace(0, selected_padding, num_frames):
            img = create_image_with_overlay("question_done.png", f"./choice_{choice_idx}.png", overlay_shift=(-selected_padding + round(idx)), v_padding=v_padding)
            images.append(img)
        img.save("question_done.png")
        v_padding += v_padding_step

    return images


def generate_answer_image(bg_image, checkmark_path, answer_image_path, answer_idx, choices, font_path, font_size=50, padding=50, v_padding=700, v_padding_step=120):
    bg_image.save("question_done.png")
    answer_img_path = f"choice_{answer_idx}.png"
    add_text_to_image(answer_image_path, answer_img_path, choices[answer_idx], (3*padding, 20), font_path, font_size=font_size, text_color=(255, 255, 255))
    img = create_image_with_overlay("question_done.png", f"choice_{answer_idx}.png", overlay_shift=0, v_padding=v_padding + answer_idx * v_padding_step)
    checkmark_img = Image.open(checkmark_path).resize((75, 75))  # Resize as needed
    h_padding = 50
    overlay_shift = 0
    checkmark_position = (2*h_padding+overlay_shift,v_padding + answer_idx * v_padding_step + 10)
    img.paste(checkmark_img, checkmark_position, checkmark_img)

    return img

def generate_final_video(video_name, video_list):
    # Concatenate the videos
    final_video = concatenate_videoclips(video_list)

    # Write the result to a file
    final_video.write_videofile(video_name)