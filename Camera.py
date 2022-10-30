import numpy as np
import threading
import math
import time
# import sys
import cv2

def version():
    print("1.0.0 Galimi")

class Camera:
    def __init__(self,  id=0, name="default", offsetX=0, offsetY=0, angle=0, exposure=0, captureapi=0):
        """
        The function __init__ is a constructor that initializes the class variables name, id, capture,
        
        :param id: The id of the camera (source)
        :param name: The name of the camera
        :param offsetX: The X offset of the camera from the center of the robot (top down view) in inches
        :param offsetY: The Y offset of the camera from the center of the robot (top down view) in inches
        :param angle: the angle of the camera in degrees
        :param exposure: the exposure of the camera
        """
        self.name = name
        print(f"{self.name} camera loading...")
        self.id = id
        self.exposure = exposure
        self.capture_api = captureapi
        self.configure_capture()
        self.x = offsetX
        self.y = offsetY
        self.angle = angle
        self.is_saving_video = False
        self.update_func = lambda: True
        self.key_callbacks = []
        self.graphics = []
        print(f"{self.name} camera loaded")

    def configure_capture(self):
        self.capture = cv2.VideoCapture(self.id, self.capture_api)

        self.capture.set(3, 640)
        self.capture.set(4, 480)

        self.capture.set(cv2.CAP_PROP_EXPOSURE,self.exposure)
        self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,-1)
        if (not(self.capture.isOpened())):
	        print("Error reading video file")

        # print("API> "+self.capture.getBackendName())

        # self.capture.set(cv2.CV_E, 0)
        self.width = int(self.capture.get(3))
        self.height = int(self.capture.get(4))

    def add_pipeline(self, pipeline):
        self.pipeline = pipeline

    def add_update_func(self, func):
        self.update_func = func

    def save_video(self, boolean):
        if boolean:
            self.video_writer = cv2.VideoWriter(f'video_{self.file_suffix()}.avi',
						cv2.VideoWriter_fourcc(*'MJPG'),
						10, (self.width, self.height))
        else:
            if self.video_writer:
                self.video_writer.release()
            self.video_writer = None
        self.is_saving_video = boolean

    def snapshot(self):
        cv2.imwrite(f"snapshot_{self.file_suffix()}.jpg", self.frame)

    def file_suffix(self):
        # sys. TODO get current directory?
        return self.name + "_" + time.strftime("%Y-%m-%d_%H-%M-%S")

    def add_key_callback(self, key, callback):
        self.key_callbacks.append((key, callback))

    def add_graphics(self, graphic):
        self.graphics.append(graphic)

    def get_object_poses(self):  
        # TODO calculate
        poses = []
        positions = self.pipeline.get_distances_and_angle_from_camera()
        
        for position in positions:
            # add camera position to measured position after adjusting measured position based on camera angle
            angle = self.angle
            x = self.x
            y = self.y
            poses.append((x, y))
        return poses

    def start(self):
        print("Starting " + self.name)
        self.thread = threading.Thread(target=self.loop)
        self.thread.start()

    def loop(self):
        while True:
            ret, frame = self.capture.read()

            self.frame = np.array(frame)

            if self.is_saving_video and self.video_writer:
                self.video_writer.write(self.frame)
                
            if len(self.graphics) > 0:
                for graphic in self.graphics:
                    graphic.display(self.name, np.copy(self.frame))

            try:
                self.pipeline.run(self.frame, self.name)
            except Exception as e: 
                print(e)
                self.configure_capture()


            self.update_func()

            # TODO check if is number instead
            # if isinstance(self.id, str):
            #     time.sleep(0.08)

            key = cv2.waitKey(1)
            if key == 27:
                break
            for pair in self.key_callbacks:
                if (key == pair[0]):
                    pair[1](self)
        # cv2.destroyAllWindows() #TODO ?

    def save_camera_settings(self):
        with open(f"{self.name}_camera.config", "w+") as f:
            string = ""
            string += f"auto_exposure: {self.capture.get(cv2.CAP_PROP_AUTO_EXPOSURE)}\n"
            string += f"auto_wb: {self.capture.get(cv2.CAP_PROP_AUTO_WB)}\n"
            string += f"brightness: {self.capture.get(cv2.CAP_PROP_BRIGHTNESS)}\n"
            string += f"saturation: {self.capture.get(cv2.CAP_PROP_SATURATION)}\n"
            string += f"fps: {self.capture.get(cv2.CAP_PROP_FPS)}\n"
            f.write(string)