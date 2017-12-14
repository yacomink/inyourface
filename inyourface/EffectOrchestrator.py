import sys
import urllib
import cStringIO
import hashlib, pprint
import os
from subprocess import call
import random
from PIL import Image, ImageDraw
import math
import inyourface.effect
from tempfile import NamedTemporaryFile

import io
import os

from inyourface.Animator import Animator

class EffectOrchestrator(Animator):
    
    frames = range(0,9)
    name = "multi"
    delay = 24

    def __init__(self, url, destdir, cache_dir, effects):
        Animator.__init__(self, url, destdir, cache_dir)
        self.effects = effects
        self.effect_processors = []
        max_frames = 1
        for e in effects:
            try:
                effect_module = getattr(inyourface.effect, e[0].upper() + e[1:])
                effect_processor = effect_module.EffectAnimator(url, destdir, cache_dir);
                if (len(effect_processor.frames) > max_frames):
                    max_frames = len(effect_processor.frames)
                self.effect_processors.append(effect_processor)

            except Exception as ex:
                print "No such " + e

        if max_frames > 1:
            self.frames = range(0, max_frames)
        self.total_frames = max_frames

        hasher = hashlib.sha1()
        hasher.update(self.__class__.name)
        hasher.update(":".join(effects))
        hasher.update(','.join(url))

        self.hash = hasher.hexdigest()

    def set_cache_provider(self, provider):
        self.cache_provider = provider
        for effect_processor in self.effect_processors:
            effect_processor.set_cache_provider(provider)

    def manipulate_frame(self, frame_image, faces, index):
        for effect_processor in self.effect_processors:
            effect_processor.total_frames = self.total_frames
            effect_processor.secondary_image = self.secondary_image
            effect_processor.secondary_imdata = self.secondary_imdata
            frame_image = effect_processor.manipulate_frame(frame_image, faces, index)

        return frame_image

