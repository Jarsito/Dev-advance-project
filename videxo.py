from moviepy.editor import VideoFileClip

# Función para reproducir video
def play_video(video_file):
    clip = VideoFileClip(video_file)
    clip.preview()

# Reproduce los videos
if __name__ == "__main__":
    play_video('C:/Users/USER/Documents/GitHub/Dev-advance-project/video/Cinematica 1.mp4')
