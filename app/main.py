import utils as utils
from PIL import ImageFont, Image
# code lines
code_lines = ['numbers = [1, 2, 3, 4, 5]', 'result = [n * 2 for n in numbers', '        if n % 2 == 1]', 'print(result)', '', "", "# what is the result?"]
# Define the choices
choices = ["A. [2, 4, 6, 8, 10]", "B. [2, 6, 10]", "C. [1, 3, 5, 7, 9]", "D. [3, 5, 7]"]
answer_idx = 1
level = "INTERMEDIATE"
level_color = '#e6b327'

# parameters
padding = 50
v_padding = 700
v_padding_step = 120

# Font settings (Adjust the path to your font file)
font_path = "./assets/fonts/ARLRDBD.ttf"  # Adjust this path to the font you want to use
font_size = 55
font = ImageFont.truetype(font_path, font_size)

# window code animation
background_image_path = './assets/background_images/3.jpg'
overlay_image_path = './assets/code_window.png'
logo_path = './assets/language_logo/python.png'

window_code_images = utils.create_code_window_animation(background_image_path=background_image_path, overlay_image_path=overlay_image_path,
    font_path=font_path, logo_top_text=level, logo_top_text_color=level_color, logo_path=logo_path, logo_size=300, font_size=50, bottom_offset=500)

# generate typing effect
code_typing_images = utils.generate_code_typing_effect(code_lines, window_code_images[-1].copy(), font_path, font_size, font, padding=50, line_height_ratio = 1.2)


# choices generation
for idx, choice in enumerate(choices):
    utils.add_text_to_image("./assets/choice.png", f"choice_{idx}.png", choice, (3*padding, 20), font_path, font_size=50, text_color=(255, 255, 255))


choices_animation_images = utils.generate_choices_animation(code_typing_images[-1].copy(),  choices, v_padding = v_padding, v_padding_step = v_padding_step, num_frames = 10)

# Generating countdown clip
# image = Image.open("./question_done.png").convert("RGBA")
countdown_clip = utils.generate_countdown_timer(background_image=choices_animation_images[-1], font_path=font_path, beep_sound_path='./assets/beep_sound/1.mp3', duration=8, font_size=150, bg_color=(0, 0, 0), text_color=(255, 255, 255), fps=24, save_video=False)

# show answer
answer_img = utils.generate_answer_image(choices_animation_images[-1].copy(), './assets/checkmarks/1.png', "./assets/choice_answer.png", answer_idx, choices, font_path, padding=padding, v_padding=v_padding, v_padding_step=v_padding_step)

# generate video
audio_path = "./assets/musics/2.mp3"
window_code_images_clip = utils.create_clip("window_code_images_clip.mp4", window_code_images, fps=60, has_end_pause = False)
code_typing_images_clip = utils.create_clip("code_typing_images_clip.mp4", code_typing_images, fps=13, has_end_pause = False)
choices_animation_images_clip = utils.create_clip("choices_animation_images_clip.mp4", choices_animation_images, fps=30, has_end_pause = False)
final_section_a = utils.generate_final_video("final_a.mp4", [window_code_images_clip, code_typing_images_clip, choices_animation_images_clip], save_video=False)
answer_clip = utils.create_clip("answer_clip.mp4", [answer_img], fps=1, has_end_pause = True, last_frame_pause_per_second = 3, save_video=False)
utils.generate_final_video("final.mp4", [final_section_a, countdown_clip, answer_clip], audio_path=audio_path, save_video=True, keep_counter_sound=True)
