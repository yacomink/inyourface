import random
from PIL import Image, ImageDraw, ImageFont
import math, pprint
from sympy.geometry import Point, Polygon, Ray, Line

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "lasers"
    frames = range(0,10)

    def manipulate_frame(self, frame_image, faces, index):

        draw = ImageDraw.Draw(frame_image)
        # font = ImageFont.truetype("Gotham.ttf", 10)

        progress = 0.9 + (float(index) / float(self.total_frames) * 0.2)

        for face in faces:

            for side in ('left', 'right'):
                ((lcx, lcy), (ex, ey), (rcx, rcy)) = face.get_eye_coords(side)
                ew = int(0.25 * math.hypot(rcx - lcx, rcy - lcy))

                (x1, y1) = face.get_landmark_coords(side + '_eye')
                pan_angle = face.angles.pan + 180
                tilt_angle = face.angles.tilt + 180
                if (abs(face.angles.pan) < 10):
                    pan_angle = 180
                    if (face.angles.pan > -1):
                        tilt_angle = 270
                    else:
                        tilt_angle = 90

                tilt_angle = tilt_angle * progress
                pan_angle = pan_angle * progress

                laser_length = Point(0,0).distance(Point(frame_image.width, frame_image.height))
                if (face.angles.pan < 0):
                    x2 = x1 + (laser_length * math.cos(math.radians( pan_angle )))
                else:
                    x2 = x1 - (laser_length * math.cos(math.radians( pan_angle )))

                if (tilt_angle > 180 or abs(face.angles.pan) < 10):
                    y2 = y1 + (laser_length * math.sin(math.radians( tilt_angle )))
                else:
                    y2 = y1 - (laser_length * math.sin(math.radians( tilt_angle )))

                shadow_width = ew/2
                draw.line( [(x1, y1),(x2-ew, y2-ew)],fill='darkred', width=ew )
                draw.line( [(x1, y1),(x2+ew, y2+ew)],fill='orangered', width=ew )
                draw.line( [(x1, y1),(x2, y2)],fill='red', width=ew )

                # (ex, ey) = face.get_landmark_coords('nose_tip')
                # draw.text((ex, ey),"{}, {}, {}".format(face.angles.pan, face.angles.tilt, face.angles.roll),(255,255,255),font=font)


        return frame_image
