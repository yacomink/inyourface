import random
from PIL import Image, ImageDraw
import math
import pprint
import random

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "multi"
    frames = range(0,6)
    delay = 200
    random_face = None
    ex = 0
    ey = 0
    initial_size = 0.02
    scale_factor = 1.5

    def manipulate_frame(self, frame_image, faces, index):
        fieri = Image.open(self.__class__.get_os_path('overlays/fieri.png'))

        original_size = frame_image.size
        if (index == 0):
            self.ex = int(((random.random() * 0.6) + 0.2) * frame_image.size[0])
            self.ey = int(((random.random() * 0.6) + 0.2) * frame_image.size[1])
            self.fieri_width = frame_image.size[0] * self.initial_size
        else:
            scale = self.scale_factor * index
            self.fieri_width = frame_image.size[0] * self.initial_size * scale
            frame_image = frame_image.resize((int(original_size[0]*scale), int(original_size[1]*scale)), Image.BICUBIC)
            ( rex, rey ) = ( self.ex*scale, self.ey*scale )
            crop_coords = (
                int(rex - original_size[0]/2),
                int(rey - original_size[1]/2),
                int(rex + original_size[0]/2),
                int(rey + original_size[1]/2)
            );
            frame_image = frame_image.crop( crop_coords ).copy()

        re_width = max(int(self.fieri_width ), 1)
        re_height = max(int(self.fieri_width * 1.2), 1)
        fieri = fieri.resize((re_width, re_height), Image.BICUBIC)

        base = frame_image.copy()

        if (index > 0):
            frame_image.paste(fieri, ( int(frame_image.size[0]/2 - re_width/2), int(frame_image.size[1]/2- re_height/2) ), fieri)
        else:
            frame_image.paste(fieri, ( int(self.ex - re_width/2), int(self.ey - re_height/2) ), fieri)

        return Image.blend(base, frame_image, float(index+1) / float(self.total_frames))
