# import sounddevice as sd
# from scipy.io.wavfile import write
# import wavio as wv
# from datetime import datetime
# import cv2
# import time
# import os
# import sys

  

# freq = 44100
  
# duration = 5
  
# recording = sd.rec(int(duration * freq), 
#                    samplerate=freq, channels=2)

# sd.wait()
  
# write("recording0.wav", freq, recording)
# wv.write("recording1.wav", recording, freq, sampwidth=2)


# #############################
# #############################
# #############################



# fps = 24
# width = 864
# height = 640
# video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")

# name = (datetime.now().strftime('%Y%m%d'))
# print(name)
# # if os.path.isdir(str(name)) is False:
# #     name = random.randint(0, 1000)
# #     name = str(name)

# name = os.path.join(os.getcwd(), str(name))
# print("ALl logs saved in dir:", name)
# if not os.path.exists(name):
#     os.mkdir(name)

# else:
#     pass


# cap = cv2.VideoCapture(0)
# ret = cap.set(3, 864)
# ret = cap.set(4, 480)
# cur_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


# start = time.time()
# video_file_count = int((datetime.now().strftime('%H%M%S')))
# video_file = os.path.join(name, str(video_file_count) + ".avi")
# print("Capture video saved location : {}".format(video_file))

# # Create a video write before entering the loop
# video_writer = cv2.VideoWriter(
#     video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
# )

# while cap.isOpened():
#     start_time = time.time()
#     ret, frame = cap.read()
#     if ret == True:
#         cv2.imshow("frame", frame)
#         if time.time() - start > 10:
#             start = time.time()
#             video_file_count += 10
#             video_file = os.path.join(name, str(video_file_count) + ".avi")
#             video_writer = cv2.VideoWriter(
#                 video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
#             )
#             # No sleeping! We don't want to sleep, we want to write
#             # time.sleep(10)

#         # Write the frame to the current video writer
#         video_writer.write(frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         break
# cap.release()
# cv2.destroyAllWindows()

# ##########################


import moviepy.editor as mpe
clip = mpe.VideoFileClip("C:\\Users\\P-Cateli-01\\Documents\\RaspyProject\\20221005\\104324.avi " )
w,z = clip.size
print(w, z)
audio_bg = mpe.AudioFileClip('C:/Users/P-Cateli-01/Documents/Enregistrements audio/Enregistrement.m4a')
#final_audio = mpe.CompositeAudioClip(audio_bg)
final_clip = clip.set_audio(audio_bg)
final_clip.write_videofile('voir.mp4')
