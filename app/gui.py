import tkinter as tk
import utils as utils
from PIL import ImageFont
import random


# parameters
wait_time = 10
padding = 50
v_padding = 700
v_padding_step = 120
# Font settings (Adjust the path to your font file)
font_path = "./assets/fonts/ARLRDBD.ttf"  # Adjust this path to the font you want to use
font_size = 55
font = ImageFont.truetype(font_path, font_size)
# window code animation
image_folder_path = "./assets/background_images"
background_image_path = utils.get_random_background(image_folder_path)
checkmark_folder_path = './assets/checkmarks'
checkmark_path = utils.get_random_background(checkmark_folder_path)
overlay_image_path = './assets/code_window.png'
audio_folder_path = "./assets/musics"
audio_path = utils.get_random_audio(audio_folder_path)
channel_logo_x = random.choice([100, 980])
channel_logo_y_offset = random.choice([-20, -10, 0, 10, 20])
level_color = {
    'BEGINNER': '#3cab26',
    'INTERMEDIATE': '#e6b327',
    'ADVANCE': '#a62828'
}

language_logo_path = {
    "Python": "./assets/language_logo/python.png",
    "Javascript":"./assets/language_logo/javascript.png",
    "C": "./assets/language_logo/c.png",
    "Java": "./assets/language_logo/java.png",
    "Typescript": "./assets/language_logo/typescript.png",
    "PHP":"./assets/language_logo/php.png"
}

def insert_tab(event):
    global question_text
    question_text.insert(tk.INSERT, "")  # Insert four spaces for a tab

def generate_video():
    global options
    question = question_text.get("1.0", "end-1c")  # Get the question value
    code_lines = question.split("\n")
    choices = [f"{idx+1}) {option_entry.get()}" for idx, option_entry in enumerate(option_entries)]  # Get the option values
    code_lines.append("")
    code_lines.append("# what is the result?")
    answer_idx = options.index(answer_var.get())  # Get the selected answer
    level = level_var.get()  # Get the selected level
    language = language_var.get()  # Get the selected language
    logo_path = logo_text.get("1.0", "end-1c")

    window_code_images = utils.create_code_window_animation(background_image_path=background_image_path, overlay_image_path=overlay_image_path,
        font_path=font_path, logo_top_text=level, logo_top_text_color=level_color[level], 
        logo_path=language_logo_path[language], logo_size=300, font_size=50, bottom_offset=500, channel_logo_path=logo_path, channel_logo_x=channel_logo_x, channel_logo_y_offset=channel_logo_y_offset)

    # generate typing effect
    code_typing_images = utils.generate_code_typing_effect(code_lines, window_code_images[-1].copy(), font_path, font_size, font, padding=50, line_height_ratio = 1.2)


    # choices generation
    for idx, choice in enumerate(choices):
        utils.add_text_to_image("./assets/choice.png", f"choice_{idx}.png", choice, (3*padding, 20), font_path, font_size=50, text_color=(255, 255, 255))


    choices_animation_images = utils.generate_choices_animation(code_typing_images[-1].copy(),  choices, v_padding = v_padding, v_padding_step = v_padding_step, num_frames = 10)

    # Generating countdown clip
    # image = Image.open("./question_done.png").convert("RGBA")
    countdown_clip = utils.generate_countdown_timer(background_image=choices_animation_images[-1], font_path=font_path, beep_sound_path='./assets/beep_sound/1.mp3', duration=wait_time, font_size=150, bg_color=(0, 0, 0), text_color=(255, 255, 255), fps=24, save_video=False)

    # show answer
    answer_img = utils.generate_answer_image(choices_animation_images[-1].copy(), checkmark_path, "./assets/choice_answer.png", answer_idx, choices, font_path, padding=padding, v_padding=v_padding, v_padding_step=v_padding_step)

    # generate video
    window_code_images_clip = utils.create_clip("window_code_images_clip.mp4", window_code_images, fps=60, has_end_pause = False)
    code_typing_images_clip = utils.create_clip("code_typing_images_clip.mp4", code_typing_images, fps=13, has_end_pause = False)
    choices_animation_images_clip = utils.create_clip("choices_animation_images_clip.mp4", choices_animation_images, fps=30, has_end_pause = False)
    final_section_a = utils.generate_final_video("final_a.mp4", [window_code_images_clip, code_typing_images_clip, choices_animation_images_clip], save_video=False)
    answer_clip = utils.create_clip("answer_clip.mp4", [answer_img], fps=1, has_end_pause = True, last_frame_pause_per_second = 3, save_video=False)
    utils.generate_final_video("final.mp4", [final_section_a, countdown_clip, answer_clip], audio_path=audio_path, save_video=True, keep_counter_sound=True)

    pass

# Create the main window
root = tk.Tk()
root.title("Video Generation GUI")

# Question
question_label = tk.Label(root, text="Question:")
question_label.pack()
question_text = tk.Text(root, height=5, width=50, padx=20, pady=20, tabs='0.5c')
question_text.pack()
question_text.bind("<Tab>", insert_tab)

# Options
options = ["Option 1", "Option 2", "Option 3", "Option 4"]
option_entries = []
for i in range(4):
    option_label = tk.Label(root, text=f"Option {i+1}:")
    option_label.pack()
    option_entry = tk.Entry(root)
    option_entry.pack()
    option_entries.append(option_entry)

# Answer Selection
answer_label = tk.Label(root, text="Answer:")
answer_label.pack()
answer_var = tk.StringVar(root)
answer_dropdown = tk.OptionMenu(root, answer_var, *options)
answer_dropdown.pack()

# Level Selection
level_label = tk.Label(root, text="Level:")
level_label.pack()
level_var = tk.StringVar(root)
level_dropdown = tk.OptionMenu(root, level_var, "BEGINNER", "INTERMEDIATE", "ADVANCE")
level_dropdown.pack()


# language selection
language_label = tk.Label(root, text="Language:")
language_label.pack()
language_var = tk.StringVar(root)
language_dropdown = tk.OptionMenu(root, language_var, "Python", "Javascript", "C", "Java", "Typescript", "PHP")
language_dropdown.pack()


# channel logo_path
logo_label = tk.Label(root, text="Logo path:")
logo_label.pack()
logo_text = tk.Text(root, height=1, width=40)
logo_text.insert(tk.END, "./assets/logo.png")
logo_text.pack()
# Button to Generate Video
generate_button = tk.Button(root, text="Generate Video", command=generate_video)
generate_button.pack()

# Run the main event loop
root.mainloop()
