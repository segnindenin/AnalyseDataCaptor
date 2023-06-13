# import cv2
# import time
# import os
# import threading
# import pyaudio
# import wave
# import keyboard
# import datetime

# my_lock = threading.RLock()
# lock = threading.Lock()

# FolderCur = 'C:\\Users\\user\\deep_learning\\ANPR\\RoadTrafic\\' + str(datetime.datetime.now().strftime('DocArchive_%Y-%m-%d'))
# print(FolderCur)
# FolderCur = os.path.join(os.getcwd(), str(FolderCur))
# print("ALl logs saved in dir:", FolderCur)
# if not os.path.exists(FolderCur):
#     os.mkdir(FolderCur)
# else:
#     pass

# def videorecord():
#     # global FolderCur
#     lock.acquire()
#     fps = 24
#     video_codec = cv2.VideoWriter_fourcc("D", "I", "V", "X")
#     cap = cv2.VideoCapture(0)
#     ret = cap.set(3, 1080)
#     ret = cap.set(4, 720)
#     start = time.time()
#     namespecial = datetime.datetime.now().strftime('%H-%M-%S')
#     video_file_count = int((datetime.datetime.now().strftime('%H%M%S')))
#     video_file = os.path.join(FolderCur, f"coupon_{namespecial}.avi")
#     print("Capture video saved location : {}".format(video_file))

#     video_writer = cv2.VideoWriter(
#         video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
#     )
#     lock.release()
#     while cap.isOpened():
#         start_time = time.time()
#         ret, frame = cap.read()
#         if ret == True:
#             cv2.imshow("frame", frame)
#             if time.time() - start > 60:
#                 namespecial = datetime.datetime.now().strftime('%H-%M-%S')
#                 start = time.time()
#                 video_file_count += 60
#                 video_file = os.path.join(FolderCur, f"coupon_{namespecial}.avi")
#                 video_writer = cv2.VideoWriter(
#                     video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
#                 )
#                 # No sleeping! We don't want to sleep, we want to write
#                 # time.sleep(10)

#             # Write the frame to the current video writer
#             video_writer.write(frame)
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#         else:
#             break
#     cap.release()
#     cv2.destroyAllWindows()

# #############################

# def audiorecord():
#     CHUNK = 1024 # Taille de chaque bloc audio
#     FORMAT = pyaudio.paInt16 # Format d'échantillonnage
#     CHANNELS = 1 # Nombre de canaux audio
#     RATE = 44100 # Taux d'échantillonnage (en Hz)
#     RECORD_SECONDS = 60 # Durée de chaque enregistrement (en secondes)

#     audio = pyaudio.PyAudio()
#     stream = audio.open(format=FORMAT, channels=CHANNELS,
#                         rate=RATE, input=True,
#                         frames_per_buffer=CHUNK)
    
#     lock.acquire()
#     while True:
#         # Enregistrement audio
#         namespecial = str(datetime.datetime.now().strftime('%H-%M-%S'))
#         frames = []
#         for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#             data = stream.read(CHUNK)
#             frames.append(data)
#             if keyboard.is_pressed('esc'):
#                 print("Exiting loop...")
#                 break
#         # Écriture du fichier audio
#         wf = wave.open(f'{FolderCur}/coupon_{namespecial}.mp3', 'wb')
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(audio.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(b''.join(frames))
#         wf.close()
#         # Attente de 30 secondes avant le prochain enregistrement
#         if keyboard.is_pressed('esc'):
#             print("Exiting loop...")
#             break
#     stream.stop_stream()
#     stream.close()
#     audio.terminate()
#     lock.release()

# th1 = threading.Thread(target=videorecord)
# th2 = threading.Thread(target=audiorecord)

# th1.start()
# # time.sleep(1)
# th2.start()

# th1.join()
# th2.join()

import concurrent.futures
import threading
import cv2
import time
import subprocess
import os
import pyaudio
import wave
import keyboard
import datetime
from moviepy.editor import VideoFileClip, AudioFileClip


FolderCur = 'C:\\Users\\user\\deep_learning\\ANPR\\RoadTrafic\\' + str(datetime.datetime.now().strftime('DocArchive_%Y-%m-%d'))
print(FolderCur)
FolderCur = os.path.join(os.getcwd(), str(FolderCur))
print("ALl logs saved in dir:", FolderCur)
if not os.path.exists(FolderCur):
    os.mkdir(FolderCur)
else:
    pass

    
my_lock = threading.RLock()
lock = threading.Lock()

# Event for synchronization
event = threading.Event()

# Fonction 1
def videorecord():
    # global FolderCur
    # lock.acquire()
    fps = 30
    video_codec = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    cap = cv2.VideoCapture(0)
    ret = cap.set(3, 1080)
    ret = cap.set(4, 720)
    namespecial = datetime.datetime.now().strftime('%H-%M')
    # video_file_count = int((datetime.datetime.now().strftime('%H%M%S')))
    video_file = os.path.join(FolderCur, f"coupon_{namespecial}.avi")
    print("Capture video saved location : {}".format(video_file))

    # event.set()
    video_writer = cv2.VideoWriter(
        video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
    )
    # event.set()
    start = time.time()
    # lock.release()
    while cap.isOpened():
        # start = time.time()
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow("frame", frame)
            if time.time() - start > 60:
                namespecial = datetime.datetime.now().strftime('%H-%M')
                start = time.time()
                # video_file_count += 60
                video_file = os.path.join(FolderCur, f"coupon_{namespecial}.avi")
                video_writer = cv2.VideoWriter(
                    video_file, video_codec, fps, (int(cap.get(3)), int(cap.get(4)))
                )
            if os.path.exists(f"{FolderCur}/coupon_{namespecial}.avi"):
                event.set()
                namespecial = 0
                # lock.release()
                # No sleeping! We don't want to sleep, we want to write
                # time.sleep(10)

            # Write the frame to the current video writer
            video_writer.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

# Fonction d'enregistrement audio
def record_audio():
    # Paramètres audio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    # Initialiser PyAudio
    audio = pyaudio.PyAudio()

    # Ouvrir un flux audio
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    # Événement pour contrôler l'arrêt de l'enregistrement
    event.wait()
    # event = threading.Event()
    event.clear()
    # Créer un nouvel enregistrement audio
    while True:
        namespecial = str(datetime.datetime.now().strftime('%H-%M'))
        frames = []
    # Enregistrer jusqu'à ce que l'événement soit déclenché
        while not event.is_set():
            data = stream.read(CHUNK)
            frames.append(data)
            if keyboard.is_pressed('esc'):
                print("Exiting loop...")
                break
    # Sauvegarder l'enregistrement audio dans un fichier WAV
        wf = wave.open(f'{FolderCur}/coupon_{namespecial}.mp3', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        event.clear()
        # Attente de 30 secondes avant le prochain enregistrement
        if keyboard.is_pressed('esc'):
            print("Exiting loop...")
            break
    stream.stop_stream()
    stream.close()
    audio.terminate()
    # lock.release()

# Fonction 3
def fonction3():
    print("Fonction 3 en cours d'exécution")
    event.wait()
    # event.clear
    
    # time.sleep(60)
    while True:
        # event.wait()
        hr = datetime.datetime.now().strftime('%H')
        mn = int(datetime.datetime.now().strftime('%M'))-1
        filevideo = f"{FolderCur}/coupon_{hr}-{mn}.avi"
        fileaudio = f"{FolderCur}/coupon_{hr}-{mn}.mp3"
        videofinal = f"{FolderCur}/coupon_{hr}-{mn}.mp4"
        # namefinal = f'{hr}-{mn}'
        if keyboard.is_pressed('esc'):
            print("Exiting loop...")
            break
        
        if os.path.exists(filevideo) and os.path.exists(fileaudio):
            # if keyboard.is_pressed('esc'):
            #     print("Exiting loop...")
            #     break
            print("c'est bon")


            print('jusquici')
            cmd = f"ffmpeg -i {filevideo} -i {fileaudio} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {videofinal}"
            subprocess.call(cmd, shell=True)
            print('aprèsla')
            os.remove(fileaudio)
            os.remove(filevideo)
            # event.clear()
    print('je me casse')
        

# Exécution des fonctions en parallèle
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Démarrer les fonctions en parallèle
    fut1 = executor.submit(videorecord)
    fut2 = executor.submit(record_audio)
    fut3 = executor.submit(fonction3)

    # Attendre que toutes les fonctions se terminent
    concurrent.futures.wait([fut1, fut2, fut3])