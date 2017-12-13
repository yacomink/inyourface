import random
from PIL import Image, ImageDraw
import math

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "googly"

    def manipulate_frame(self, frame_image, faces, index):
        # Instantiates a client
        googly_eye = Image.open(self.__class__.get_os_path('overlays/eye.png'))

        for face in faces:

            for side in ('left', 'right'):

                ((lcx, lcy), (ex, ey), (rcx, rcy)) = face.get_eye_coords(side)

                ew = int(1.5 * math.hypot(rcx - lcx, rcy - lcy))

                pasted = googly_eye.rotate(random.randint(0, 360), Image.BICUBIC).resize((ew, ew), Image.BICUBIC)
                frame_image.paste(pasted, (int(ex - ew/2), int(ey - ew/2)), pasted)

        return frame_image
