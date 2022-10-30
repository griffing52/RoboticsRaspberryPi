from NTConnection import NTConnection
from Pipeline import *
from Camera import Camera
from time import sleep
import math

pipeline = BallDetection()

camera = Camera("C:/Users/griff/Documents/Programming/Python/OpenCV/filename4.avi")
camera.add_pipeline(pipeline)

camera.add_key_callback(ord('v'), lambda this: this.save_video(not(this.is_saving_video)))
camera.add_key_callback(ord('s'), lambda this: this.snapshot())


nt = NTConnection("127.0.0.1")
entry = nt.instance.getEntry("cargo")

camera.start()