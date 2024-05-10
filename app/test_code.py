# import utils as utils
# from PIL import ImageFont, Image

# # code_lines = ['print("".join(list[::2]))']


# # res = utils.preprocess_line(code_lines[0])
# # print(res)

# # exit()
# # code lines
# code_lines = ['list = ["a", "b", "c", "d"]', 'print( "".join( list[::2] ) )',"", "# what is the result?"]
# # Define the choices
# choices = ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4']
# answer_idx = 0

# # parameters
# padding = 50
# v_padding = 700
# v_padding_step = 120

# # Font settings (Adjust the path to your font file)
# font_path = "./assets/fonts/ARLRDBD.ttf"  # Adjust this path to the font you want to use
# font_size = 55
# font = ImageFont.truetype(font_path, font_size)

# # window code animation
# background_image_path = './assets/background_images/1.jpg'
# overlay_image_path = './assets/code_window.png'
# logo_path = './assets/language_logo/python.png'
# # window_code_images = utils.create_code_window_animation(background_image_path=background_image_path, overlay_image_path=overlay_image_path)


# window_code_images = utils.create_image_with_overlay(background_image_path, overlay_image_path, overlay_shift=0, font_path=font_path,
#     logo_top_text="", logo_bottom_text="Advanced", logo_bottom_text_color="green", logo_path=logo_path, logo_size=300, font_size=50, bottom_offset=500)

# # generate typing effect
# code_typing_images = utils.generate_code_typing_effect(code_lines, window_code_images.copy(), font_path, font_size, font, padding=50, line_height_ratio = 1.2)


# code_typing_images[-1].show()
# exit()
# # # choices generation
# # for idx, choice in enumerate(choices):
# #     utils.add_text_to_image("./assets/choice.png", f"choice_{idx}.png", choice, (3*padding, 20), font_path, font_size=50, text_color=(255, 255, 255))


# # choices_animation_images = utils.generate_choices_animation(code_typing_images[-1].copy(),  choices, v_padding = v_padding, v_padding_step = v_padding_step, num_frames = 10)


# # # show answer
# # answer_img = utils.generate_answer_image(choices_animation_images[-1].copy(), './assets/checkmarks/1.png', "./assets/choice_answer.png", 3, choices, font_path, padding=padding, v_padding=v_padding, v_padding_step=v_padding_step)


# # # generate video
# # window_code_images_clip = utils.create_clip("window_code_images_clip.mp4", window_code_images, fps=60, has_end_pause = False, last_frame_pause_per_second = 2, save_video=False)
# # code_typing_images_clip = utils.create_clip("code_typing_images_clip.mp4", code_typing_images, fps=10, has_end_pause = True, last_frame_pause_per_second = 2, save_video=False)
# # choices_animation_images_clip = utils.create_clip("choices_animation_images_clip.mp4", choices_animation_images, fps=30, has_end_pause = True, last_frame_pause_per_second = 20, save_video=False)
# # answer_clip = utils.create_clip("answer_clip.mp4", [answer_img], fps=1, has_end_pause = True, last_frame_pause_per_second = 5, save_video=False)
# # utils.generate_final_video("final.mp4", [window_code_images_clip, code_typing_images_clip, choices_animation_images_clip, answer_clip])


from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_audioclips, CompositeAudioClip
import utils as utils
from moviepy.editor import ImageSequenceClip, VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, ImageClip

# Load the video file
final_a = VideoFileClip('final_a.mp4')
counter_video = VideoFileClip('counter_video.mp4')
answer_clip = VideoFileClip('answer_clip.mp4')


def generate_final_video(video_name, video_list, audio_path=None, save_video=False):
    # Concatenate the videos
    final_video = utils.concatenate_videoclips(video_list)

    # If an audio path is provided, load it
    if audio_path:
        final_audio = AudioFileClip(audio_path)
        final_audio = final_audio.set_duration(final_video.duration)
        final_audio_fadeout = final_audio.subclip(0, video_list[0].duration+2).audio_fadeout(4)  # 2 seconds fade out
        final_audio_fadein = final_audio.subclip(video_list[0].duration+video_list[1].duration, final_audio.duration).audio_fadein(2)
        correct_answer_audio = AudioFileClip("./assets/correct_answer/1.mp3")
        # Combine the audio clips with fade effects
        combined_audio = CompositeAudioClip([final_audio_fadeout.set_end(video_list[0].duration+2),  
            video_list[1].audio.set_start(video_list[0].duration).set_end(video_list[0].duration+video_list[1].duration), 
            correct_answer_audio.set_start(video_list[0].duration+video_list[1].duration),
            final_audio_fadein.set_start(video_list[0].duration+video_list[1].duration).set_end(final_audio.duration)])


    # Set the audio of the final video to be the combined audio
    final_video = final_video.set_audio(combined_audio)

    # Write the result to a file
    if save_video:
        final_video.write_videofile(video_name, codec='libx264', audio_codec='aac')

    return final_video

audio_path = "./assets/musics/2.mp3"
generate_final_video('test.mp4', [final_a, counter_video, answer_clip], audio_path=audio_path, save_video=True)