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

import io
import os

from inyourface.Face import Face
from google.cloud import vision

class Animator(object):
    
    frames = range(0,9)
    name = "base"
    delay = 24

    def __init__(self, url, destdir):
        self.vision_client = vision.Client()
        self.url = url
        self.destdir = destdir
        self.raw_frames = []

        hasher = hashlib.sha1()
        hasher.update(self.__class__.name)
        hasher.update(url)

        self.hash = hasher.hexdigest()

    def manipulate_frame(self, frame_image, faces, index):
        raise NotImplementedError( "Should have implemented this" )

    def generate_frames_from_animation(self): 
        frames = []
        nframes = 0
        while self.image:
            try:
                self.image.seek( nframes )
            except EOFError:
                break;
        
            # extract frame
            frame_image = self.image.convert('RGBA')
            frames.append(NamedTemporaryFile(suffix='.gif'))
            frame_image.save(frames[-1].name, 'GIF')
            with io.open(frames[-1].name, 'rb') as image_file:
                content = image_file.read()

            image = self.vision_client.image(content=content)
            faces = self.transform_faces(image.detect_faces())

            frame_image = self.manipulate_frame( frame_image, faces, nframes )
            self.raw_frames.append(frame_image)

            frames[-1] = NamedTemporaryFile(suffix='.gif')
            frame_image.save(frames[-1])
            nframes += 1

        return frames

    def generate_frames_from_image(self): 

        frames = []
        for (i) in self.__class__.frames:
        
            image = self.vision_client.image(content=self.imdata)

            faces = self.transform_faces(image.detect_faces())

            out = self.manipulate_frame( self.image.copy(), faces, i )
            self.raw_frames.append(out)

            frames.append(NamedTemporaryFile(suffix='.gif'))
            out.save(frames[-1])

        return frames

    def transform_faces(self, faces):
        return map(lambda face: Face.from_google_face(face), faces)

    def gif(self):

        self.imdata = urllib.urlopen(self.url).read()
        self.image = Image.open(cStringIO.StringIO(self.imdata))
        self.animated_source = self.check_animated(self.image)

        if (self.animated_source):
            self.total_frames = self.animated_source
            frames = self.generate_frames_from_animation()
            cmd = "/usr/bin/gifsicle --delay=24 -l0 --colors 255"
        else:
            self.total_frames = len(self.__class__.frames)
            frames = self.generate_frames_from_image()
            cmd = "/usr/bin/gifsicle --delay=" + str(self.__class__.delay) + " -l0 --colors 255"

        if (self.total_frames == 1 and not self.animated_source):
            outname = self.destdir + self.__class__.name + "/" + self.hash + ".jpg"
            self.raw_frames[-1].save(outname)
            return outname

        for (file) in frames:
            cmd += " " + file.name

        outname = self.destdir + self.__class__.name + "/" + self.hash + ".gif"
        cmd += " > " + outname

        call(cmd, shell=True)
        return outname

    def check_animated(self, img):
        try:
            img.seek(1)
        except (EOFError):
            return 0
        frames = 0
        while img:
            try:
                img.seek( frames )
                frames += 1
            except EOFError:
                break;
        img.seek(0)
        return frames


