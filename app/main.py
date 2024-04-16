import utils as utils
from PIL import ImageFont, Image
# code lines
code_lines = ['list = ["a", "b", "c", "d"]', 'print( "".join( list[::2] ) )',"", "", "", "# what is the result?"]
# Define the choices
choices = ["A) 'ac'", "B) 'bd'", "C) 'abcd'", "D) 'dcba'"]
answer_idx = 0
level = "INTERMEDIATE"

# parameters
padding = 50
v_padding = 700
v_padding_step = 120

# Font settings (Adjust the path to your font file)
font_path = "./assets/fonts/ARLRDBD.ttf"  # Adjust this path to the font you want to use
font_size = 55
font = ImageFont.truetype(font_path, font_size)

# window code animation
background_image_path = './assets/background_images/1.jpg'
overlay_image_path = './assets/code_window.png'
logo_path = './assets/language_logo/python.png'

window_code_images = utils.create_code_window_animation(background_image_path=background_image_path, overlay_image_path=overlay_image_path,
    font_path=font_path, logo_top_text=level, logo_top_text_color="yellow", logo_path=logo_path, logo_size=300, font_size=50, bottom_offset=500)

# generate typing effect
code_typing_images = utils.generate_code_typing_effect(code_lines, window_code_images[-1].copy(), font_path, font_size, font, padding=50, line_height_ratio = 1.2)


# choices generation
for idx, choice in enumerate(choices):
    utils.add_text_to_image("./assets/choice.png", f"choice_{idx}.png", choice, (3*padding, 20), font_path, font_size=50, text_color=(255, 255, 255))


choices_animation_images = utils.generate_choices_animation(code_typing_images[-1].copy(),  choices, v_padding = v_padding, v_padding_step = v_padding_step, num_frames = 10)


# show answer
answer_img = utils.generate_answer_image(choices_animation_images[-1].copy(), './assets/checkmarks/1.png', "./assets/choice_answer.png", answer_idx, choices, font_path, padding=padding, v_padding=v_padding, v_padding_step=v_padding_step)

# generate video
window_code_images_clip = utils.create_clip("window_code_images_clip.mp4", window_code_images, fps=60, has_end_pause = False, last_frame_pause_per_second = 2, save_video=False)
code_typing_images_clip = utils.create_clip("code_typing_images_clip.mp4", code_typing_images, fps=10, has_end_pause = True, last_frame_pause_per_second = 2, save_video=False)
choices_animation_images_clip = utils.create_clip("choices_animation_images_clip.mp4", choices_animation_images, fps=30, has_end_pause = True, last_frame_pause_per_second = 30, save_video=False)
answer_clip = utils.create_clip("answer_clip.mp4", [answer_img], fps=1, has_end_pause = True, last_frame_pause_per_second = 5, save_video=False)
utils.generate_final_video("final.mp4", [window_code_images_clip, code_typing_images_clip, choices_animation_images_clip, answer_clip], audio_path="./assets/musics/1.mp3")