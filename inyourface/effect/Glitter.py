import random
from PIL import Image, ImageDraw
import math, numpy
import inspect, os

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "glitter"

    def manipulate_frame(self, frame_image, faces, index):
        sparkles = [
            Image.open(self.__class__.get_os_path('overlays/sparkle_1.png')),
            Image.open(self.__class__.get_os_path('overlays/sparkle_2.png')),
            Image.open(self.__class__.get_os_path('overlays/sparkle_3.png'))
        ]

        for face in faces:
            sparkle = sparkles[index%3]

            (lx, ly) = face.get_landmark_coords('left_of_left_eyebrow')
            (rx, ry) = face.get_landmark_coords('right_of_right_eyebrow')

            size = sparkle.size
            x = size[0]
            y = size[1]

            # width between eyebrows
            ew = abs(rx-lx)

            sparkle.thumbnail((ew,ew), Image.ANTIALIAS)
            sw = sparkle.size[0] # sparkle width
            sh = sparkle.size[1] # sparkle height
            rat = 1.75 # size increase ratio
            sparkle = sparkle.resize((int(sw*rat), int(sh*rat)), Image.BICUBIC)
            sw = sparkle.size[0] # sparkle width
            sh = sparkle.size[1] # sparkle height

            rot = self.__class__.angle(lx, ly, rx, ry)

            sparkle = sparkle.rotate(rot)
            frame_image.paste(sparkle, (int(lx-sw/4), int(ly - sh)), sparkle)

        return frame_image

    @staticmethod
    def coefficient(pa, pb):
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

        A = numpy.matrix(matrix, dtype=numpy.float)
        B = numpy.array(pb).reshape(8)

        res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
        return numpy.array(res).reshape(8)

    @staticmethod
    def angle( x1, y1, x2, y2 ):
        dx = x2 - x1
        dy = y2 - y1
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        return math.degrees(rads)
