import random
from PIL import Image, ImageDraw
import math
import inspect, os

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "deal"

    def manipulate_frame(self, frame_image, faces, index):
        # Instantiates a client

        glasses = Image.open(self.__class__.get_os_path('overlays/glasses.png'))

        for face in faces:

            (lx, ly) = face.get_landmark_coords('left_eye_left_corner')
            (rx, ry) = face.get_landmark_coords('right_eye_right_corner')

            ew = int((rx - lx) * 0.6)

            start = -1 * ew
            end = ly - ew/3

            progress = float(index+1) / float(self.total_frames * 0.7)
            height = start + progress * (end - start)
            if (height > end):
                height = end

            #increase ratio
            ir = 1.5
            # width between eyes times ratio to increase size
            we = abs(rx-lx)*ir

            glasses.thumbnail((we,we), Image.ANTIALIAS)
            gs = glasses.size
            gsx = gs[0]
            gsy = gs[1]
            x = lx + abs((rx-lx)/2.0) - abs(gsx/2.0)

            rot = self.__class__.angle(lx, ly, rx, ry)
            pasted = glasses.rotate(rot, expand=True)
            frame_image.paste(pasted, (int(x), int(height)), pasted)

        return frame_image

    # add a util lib sometime
    @staticmethod
    def angle( x1, y1, x2, y2 ):
        dx = x2 - x1
        dy = y2 - y1
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        return math.degrees(rads)
