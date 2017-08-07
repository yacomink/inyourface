import random
from PIL import Image, ImageDraw
import math

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "gray"

    def manipulate_frame(self, frame_image, faces, index):
        frame_image = frame_image.convert('L')
        return frame_image

