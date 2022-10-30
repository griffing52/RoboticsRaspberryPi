import numpy as np
import imutils
import cv2

class Pipeline:
    def __init__(self):
        self.id = id

    def get_distances_and_angle_from_camera(self):
        return [(0, 0)]

    def run(self, frame):
        return


class BallDetection(Pipeline):
    def __init__(self):
        Pipeline.__init__(self)
        # test widths (pixels)
        self.positions = [(50, 0), (100, 10), (20, -6)]
        self.lower_threshold = np.array([  1, 120,  100]) # home red bouncy ball
        self.upper_threshold = np.array([  4, 222, 255])
        # self.lower_threshold = np.array([100, 159,  74]) # blue ball
        # self.upper_threshold = np.array([106, 218, 174])
    
    def get_distances_and_angle_from_camera():
        return self.positions

    def run(self, frame, name):
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        mask = cv2.inRange(hsv, self.lower_threshold, self.upper_threshold)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 15:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # cv2.imshow(name, frame)

class HubDetection(Pipeline):
    def __init__(self):
        Pipeline.__init__(self)
    
    def get_distances_and_angle_from_camera(self):
        if self.width == 0:
            return 0
        w = self.width * ((36.5)/(self.numTargets*5+(self.numTargets-1)*5.5))
        return [26691.7 / w - 60.0122]

    def run(self, frame, name):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_threshold = np.array([56, 100, 65])
        upper_threshold = np.array([74, 255, 255])
        yTolerance = 60
        threshold = cv2.inRange(hsv, lower_threshold, upper_threshold)

        kernel = np.ones((3, 3), np.uint8)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)    
        calibration = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)

        # get contours
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # init filtered array
        filtered = []
        
        # fill filtered array with values from all contours with an area greater than 15
        # respective values are the contour's center x-value, center y-value, 
        # bounding-rectangle lower-left x-val bounding-rect lower-left y-val, 
        # bounding rect upper-right x, bounding-rect upper-right y-val, and area
        for c in contours:
            area = cv2.contourArea(c)
            if (area < 25 or area > 750):
                continue
            rect = cv2.boundingRect(c)
            x,y,w,h = rect
            M = cv2.moments(c)
            # gets center x and y
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                filtered.append((cX, cY, x, x+w, y, y+h, area))

        rv = 0
        rw = 0
        rx = 0
        # if there are any values in filtered
        if len(filtered) > 0:
            # finds median value and filters for all values within the y tolerance on smart dashboard
            filtered.sort(key=lambda c: c[1]) # sorts array by y-value
            median = filtered[int(len(filtered)/2)][1] # gets median y-value
            # filtered = list(filter(lambda f: abs(median-f[1]) < yT, filtered)) # filters
            filtered = list(filter(lambda f: abs(median-f[1]) < yTolerance, filtered)) # filters


            # if there are any values left in filtered
            if len(filtered) > 1:
                # sorts filtered array by contour area and caps it to at-most 4 elements
                filtered = sorted(filtered, key=lambda f: f[6])[-4:]
                
                rv = len(filtered) # gets the amount of contours found

                if rv > 1:
                    longWidth = filtered[len(filtered)-1][3] - filtered[len(filtered)-1][2]
                    filtered = sorted(filtered, key=lambda c: c[0])
                    for i in range(len(filtered)-1, 0, -1):
                        if (filtered[i][0]-filtered[i-1][0] > longWidth*3):
                            rv+=1


                # gets lower-left-most x- and y-value and upper-right-most x- and y-value for final bounding box
                fx, fy, bx, by = filtered[0][2], filtered[0][4], filtered[0][3], filtered[0][5]
                for f in filtered:
                    if f[2] < fx: fx = f[2]
                    if f[4] < fy: fy = f[4]
                    if f[3] > bx: bx = f[3]
                    if f[5] > by: by = f[5]
                rw = bx - fx
                rx = -0.0937486*(0.5*(bx+fx)-0.5*680) - 4.99446 # x in pixels converted to angle in degrees!
                # draws bounding rectangle
                cv2.rectangle(frame,(fx, fy),(bx, by),(0,255,0),2)

                self.width = rw
                self.xOff = rx

        cv2.imshow(name, frame)