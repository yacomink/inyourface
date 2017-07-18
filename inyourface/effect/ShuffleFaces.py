import sys, os, io
import numpy as np
import cv2
import random
from google.cloud import vision

import random
from PIL import Image, ImageDraw, ImageFilter
import math

from inyourface.effect import Swap

class EffectAnimator(Swap.EffectAnimator):

    name = "shuffle"

    def manipulate_frame(self, frame_image, faces, index):
        # Read images
        dest = np.array(frame_image.convert('RGB'))
        dest_faces = faces

        source = np.array(frame_image.convert('RGB'))
        source_faces = faces[:]
        random.shuffle(source_faces)
        mask = np.zeros(dest.shape, dtype = dest.dtype)

        for j in xrange(len(faces)):
            (dest, mask) = self.pasteOne(source, dest, source_faces[ j ], dest_faces[j], mask)

        frame_image.paste(Image.fromarray(dest), mask=Image.fromarray(mask).convert('L').filter(ImageFilter.GaussianBlur(4)))
        return frame_image
