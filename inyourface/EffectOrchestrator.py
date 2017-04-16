import sys
import urllib
import cStringIO
import hashlib, pprint
import os
import simplejson as json
from subprocess import call
import random
from PIL import Image, ImageDraw
import math
from tempfile import NamedTemporaryFile
import inyourface.effect

import io
import os

from inyourface.Animator import Animator

class EffectOrchestrator(Animator):
    
    frames = range(0,9)
    name = "multi"
    delay = 24

    def __init__(self, url, destdir, effects):
        Animator.__init__(self, url, destdir)
        self.effects = effects
        self.effect_processors = []
        for e in effects:
            effect_module = getattr(inyourface.effect, e[0].upper() + e[1:])
            self.effect_processors.append(effect_module.EffectAnimator(url, destdir))


        hasher = hashlib.sha1()
        hasher.update(self.__class__.name)
        hasher.update(":".join(effects))
        hasher.update(url)

        self.hash = hasher.hexdigest()

    def manipulate_frame(self, frame_image, faces, index):
        for effect_processor in self.effect_processors:
            effect_processor.total_frames = self.total_frames
            frame_image = effect_processor.manipulate_frame(frame_image, faces, index)

        return frame_image

