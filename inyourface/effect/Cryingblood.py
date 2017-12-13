import random
from PIL import Image, ImageDraw
import math

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "cryingblood"

    def cry_frame(self, frame_image, faces, index):
        # Instantiates a client
        tear = Image.open(self.__class__.get_os_path('overlays/tearblood.png'))

        lowest = 0

        for face in faces:

            for side in ('left', 'right'):

                ((lcx, lcy), (ex, ey), (rcx, rcy)) = face.get_eye_coords(side)

                ew = int(1.25 * math.hypot(rcx - lcx, rcy - lcy))

                pasted = tear.resize((ew, ew), Image.BICUBIC)
                left_y = int(lcy + (index * ew * 1.5) + (ew * .75))
                right_y = int(rcy + (index * ew * 1.5) + (ew * .5) )
                frame_image.paste(pasted, (int(lcx - ew/2), left_y), pasted)
                frame_image.paste(pasted, (int(rcx - ew/2), right_y), pasted)
                lowest = max(left_y, right_y)

        return lowest


    def bottom_fill(self, frame_image, index):

        draw = ImageDraw.Draw(frame_image)
        increment = int(frame_image.height / 20)
        draw.rectangle( [(0,frame_image.height - index*increment), (frame_image.width,frame_image.height)], fill="#d50000" )


    def manipulate_frame(self, frame_image, faces, index):

        lowest = 0
        bottom_fill = 0
        for i in range(0, index):
            if bottom_fill > 0:
                self.bottom_fill(frame_image, index - bottom_fill)
            else:
                lowest = max(self.cry_frame(frame_image, faces, i), 0)
                if (lowest > frame_image.height):
                    bottom_fill = i

        return frame_image
