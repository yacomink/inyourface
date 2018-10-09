import random
from PIL import Image, ImageDraw
import math
import pprint
import random

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "multi"
    frames = range(0,6)
    delay = 3
    random_face = None

    def manipulate_frame(self, frame_image, faces, index):

        re_width = int(math.ceil(frame_image.width * 1.03))
        re_height = int(math.ceil(frame_image.height * 1.02))

        base = frame_image.resize((re_width, re_height), Image.BICUBIC)

        x_shift = random.randint(0, base.width - frame_image.width)
        y_shift = random.randint(0, base.height - frame_image.height)

        return base.crop( (x_shift, y_shift, frame_image.width + x_shift, frame_image.height + y_shift) )

