import numpy
import cv2

class Graphics:
    def __init__(self):
       self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def display(self, name, frame):
        self.frame = frame
        for elm in self.elements:
            self.frame = elm.draw(self.frame)

        cv2.imshow(name, self.frame)
        