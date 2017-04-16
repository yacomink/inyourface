import random
from PIL import Image, ImageDraw
import math

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "angry"
    delay = 2

    def manipulate_frame(self, frame_image, faces, index):

        draw = ImageDraw.Draw(frame_image)

        for face in faces:

            for side in ('left', 'right'):
                ((lcx, lcy), (rcx, rcy)) = face.get_paired_landmark_coords('%s_of_' + side + '_eyebrow')
                (ex, ey) = face.get_landmark_coords(side + '_eyebrow_upper_midpoint')

                ew = int(1.5 * math.hypot(rcx - lcx, rcy - lcy))
                rot = random.randint(0, 15)

                if (side == 'right'):
                    (x1, y1) = (lcx, lcy)
                    x2 = x1 + (ew * math.cos(math.radians( self.__class__.angle(lcx, lcy, rcx, rcy) - 25 - rot )))
                    y2 = y1 + (ew * math.sin(math.radians( self.__class__.angle(lcx, lcy, rcx, rcy) - 25 - rot )))

                if (side == 'left'):
                    (x1, y1) = (lcx, lcy)
                    x2 = x1 + (ew * math.cos(math.radians( self.__class__.angle(lcx, lcy, rcx, rcy) + 15 + rot )))
                    y2 = y1 + (ew * math.sin(math.radians( self.__class__.angle(lcx, lcy, rcx, rcy) + 15 + rot )))

                    delta = y2 - y1
                    y1 -= delta
                    y2 -= delta


                draw.line( [(x1, y1),(x2, y2)],fill='black', width=int(round(ew * 0.30)) )

        return frame_image

    @staticmethod
    def angle( x1, y1, x2, y2 ):
        dx = x2 - x1
        dy = y2 - y1
        rads = math.atan2(-dy,dx)
        rads %= 2*math.pi
        return math.degrees(rads)    

