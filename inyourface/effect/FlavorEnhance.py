import random
from PIL import Image, ImageDraw
import math
import pprint
import random

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "crying"
    frames = range(0,5)
    delay = 200
    random_face = None

    def manipulate_frame(self, frame_image, faces, index):
        fieri = Image.open('overlays/fieri.png')

        if (index == 0):
            self.random_face = random.choice(faces)
        ((lcx, lcy), (ex, ey), (rcx, rcy)) = self.random_face.get_eye_coords('left')

        fieri_width = (rcx - lcx) * 1.15

        scale = 1 - (float(index)/float(self.total_frames))

        img = frame_image
        idk = 1
        offsets = (0,0)
        if (index > 0):
            (idk, offsets, img) = self.crop_image(frame_image, (ex, ey), scale)

        re_width = max(int(fieri_width * idk), 1)
        re_height = max(int(fieri_width * 1.2 * idk), 1)

        fieri = fieri.resize((re_width, re_height), Image.BICUBIC)

        base = img.copy()

        if (index > 0):
            img.paste(fieri, ( int(frame_image.size[0]/2 - fieri.size[0]/2 + offsets[0]), int(frame_image.size[1]/2- fieri.size[1]/2 + offsets[1]) ), fieri)
        else:
            img.paste(fieri, ( int(ex - fieri.size[0]/2 + offsets[0]), int(ey - fieri.size[1]/2 + offsets[1]) ), fieri)

        alpha = 1 - ((index+2) * 0.2)
        pprint.pprint((scale, alpha))
        return Image.blend(img, base, max(scale - 0.3, 0))


    def crop_image(self, img, xy, scale_factor):
        '''Crop the image around the tuple xy

        Inputs:
        -------
        img: Image opened with PIL.Image
        xy: tuple with relative (x,y) position of the center of the cropped image
            x and y shall be between 0 and 1
        scale_factor: the ratio between the original image's size and the cropped image's size
        '''
        center = xy
        original_size = img.size
        offset_x = 0
        offset_y = 0

        size_down = scale_factor
        left = (int) (xy[0] - ((img.size[0] * size_down) / 2))
        right = (int) (xy[0] + ((img.size[0] * size_down) / 2))
        upper = (int) (xy[1] - ((img.size[1] * size_down) / 2))
        lower = (int) (xy[1] + ((img.size[1] * size_down) / 2))
        cropped_img = img.crop((left, upper, right, lower)).copy()
        # if (upper < 0):
        #     offset_y = upper * -1
        #     lower += offset_y
        #     upper = 0
        # if (left < 0):
        #     offset_x = left * -1
        #     right += offset_x
        #     left = 0
        # pprint.pprint((left, upper, right, lower, size_down))
        crop_scale_up = float(original_size[0]) / float(cropped_img.size[0])

        return (crop_scale_up, (offset_x, offset_y), cropped_img.resize(original_size, Image.BICUBIC))