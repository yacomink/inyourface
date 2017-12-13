import numpy as np
import sys
import urllib
import cStringIO
import hashlib, pprint
import tempfile, os
from subprocess import call
import os
import random
from PIL import Image, ImageDraw
import math
from tempfile import NamedTemporaryFile

import io
import os

from inyourface.Animator import Animator

class EffectAnimator(Animator):

    name = "thinking"

    def manipulate_frame(self, frame_image, faces, index):
        # Instantiates a client
        hand = Image.open(self.__class__.get_os_path('overlays/thinking-hand.png'))

        for face in faces:

            ((ex,ey), (rx,ry)) = face.get_paired_landmark_coords('chin_%s_gonion')

            ew = int((rx - ex) * 0.6)

            start = -1 * ew
            end = ey - ew/3

            progress = float(index+1) / float(self.total_frames * 0.7)
            height = start + progress * (end - start)
            if (height > end):
                height = end

            pasted = hand.resize((ew, ew), Image.BICUBIC).rotate(face.angles.tilt, Image.BICUBIC)
            frame_image.paste(pasted, (int(ex), int(height)), pasted)

        return frame_image
