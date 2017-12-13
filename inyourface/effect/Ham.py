import random
import cv2
from PIL import Image,ImageDraw,ImageEnhance
from tempfile import NamedTemporaryFile
import math
import numpy as np
from pprint import pprint
import inspect, os

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    frames = [0]

    name = "ham"

    dir_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + "/../.."))

    mask_elements_path = Animator.get_os_path("/overlays/ham.png")
    mask_mouth_path    = Animator.get_os_path("/overlays/juggalo-mouth.png")

    average_points = np.array([[245, 215],
           [301, 212],
           [345, 211],
           [400, 213],
           [323, 226],
           [323, 280],
           [323, 317],
           [324, 342],
           [286, 329],
           [361, 328],
           [323, 327],
           [347, 289],
           [299, 290],
           [323, 296],
           [278, 227],
           [295, 233],
           [277, 237],
           [259, 233],
           [367, 225],
           [385, 231],
           [368, 237],
           [350, 232],
           [273, 201],
           [371, 200],
           [222, 281],
           [425, 277],
           [276, 233],
           [368, 232],
           [322, 210],
           [325, 385],
           [233, 337],
           [416, 334]]) + (27,11)

    def getFacePoints(self, face):
        points = []
        for feature in ('left_of_left_eyebrow',
                        'right_of_left_eyebrow',
                        'left_of_right_eyebrow',
                        'right_of_right_eyebrow',
                        'midpoint_between_eyes',
                        'nose_tip',
                        'upper_lip',
                        'lower_lip',
                        'mouth_left',
                        'mouth_right',
                        'mouth_center',
                        'nose_bottom_right',
                        'nose_bottom_left',
                        'nose_bottom_center',
                        'left_eye_top_boundary',
                        'left_eye_right_corner',
                        'left_eye_bottom_boundary',
                        'left_eye_left_corner',
                        'right_eye_top_boundary',
                        'right_eye_right_corner',
                        'right_eye_bottom_boundary',
                        'right_eye_left_corner',
                        'left_eyebrow_upper_midpoint',
                        'right_eyebrow_upper_midpoint',
                        'left_ear_tragion',
                        'right_ear_tragion',
                        'left_eye_pupil',
                        'right_eye_pupil',
                        'forehead_glabella',
                        'chin_gnathion',
                        'chin_left_gonion',
                        'chin_right_gonion'):
            points.append( face.get_landmark_coords(feature) )

        return points

    def getTransPIL(self, imarray):
        file = NamedTemporaryFile(suffix='.png')
        cv2.imwrite(file.name, np.uint8(imarray))
        return Image.open(file.name)

    def maskFace(self, frame_image, face):

        elements = cv2.imread(self.__class__.mask_elements_path, cv2.IMREAD_UNCHANGED);
              
        h, status = cv2.findHomography(self.average_points, np.array(self.getFacePoints(face)))
        mask_elements = self.getTransPIL(cv2.warpPerspective(elements, h, (frame_image.width,frame_image.height)))
        frame_image.paste(mask_elements, (0,0), mask_elements)


    def manipulate_frame(self, frame_image, faces, index):

        for face in faces:
          self.maskFace(frame_image, face)

        return frame_image

