from moviepy.editor import AudioFileClip, CompositeAudioClip

# Load the audio clips
audio_a = AudioFileClip("./assets/musics/2.mp3")
audio_b = AudioFileClip("./assets/musics/1.mp3")

# Trim audio_a to fade out at 5 seconds
audio_a_fadeout = audio_a.subclip(0, 6).audio_fadeout(1)  # 2 seconds fade out
audio_a_fadein = audio_a.subclip(7, 10).audio_fadein(2)
# Trim audio_a to start at 5 seconds and end at 10 seconds
audio_a_fadeback = audio_a.subclip(5, 10)

# Combine the audio clips with fade effects
combined_audio = CompositeAudioClip([audio_a_fadeout.set_end(5),  audio_a_fadein.set_start(7).set_end(10)])

# Export the combined audio
combined_audio.write_audiofile("combined_audio.mp3", fps = 16000)