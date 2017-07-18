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
import sqlite3
import pickle

import io
import os

from inyourface.Face import Face
from google.cloud import vision

class Animator(object):
    
    frames = range(0,9)
    name = "base"
    delay = 24

    def __init__(self, url, destdir, cache_dir):
        self.vision_client = vision.Client()
        self.url = url[-1]
        if len(url) > 1:
            self.secondary_urls = list(url[0:-1])
        else:
            self.secondary_urls = []
        self.destdir = destdir
        self.cache_dir = cache_dir
        self.cache_connection = False
        self.raw_frames = []
        self.total_frames = len(self.__class__.frames)

        hasher = hashlib.sha1()
        hasher.update(self.__class__.name)
        hasher.update(','.join(url))

        if (self.cache_dir):
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
            conn = sqlite3.connect(self.cache_dir + 'faces.db')
            self.cache_connection = conn
            c = conn.cursor()

            # Create table
            c.execute('''CREATE TABLE IF NOT EXISTS faces
                         (facesum char(32) PRIMARY KEY, face_data text)''')
            self.cache_connection.commit()

        self.hash = hasher.hexdigest()

    def manipulate_frame(self, frame_image, faces, index):
        raise NotImplementedError( "Should have implemented this" )

    def get_faces(self, image_data):

        hasher = hashlib.md5()
        hasher.update(image_data)
        cache_key = hasher.hexdigest()
        if (self.cache_connection):
            c = self.cache_connection.cursor()
            c.execute("select * FROM faces WHERE facesum = ?", (cache_key,))
            res = c.fetchone()
            if (res):
                return pickle.loads(res[1])


        image = self.vision_client.image(content=image_data)
        faces = image.detect_faces()

        if (self.cache_connection):
            c = self.cache_connection.cursor()
            c.execute('REPLACE INTO faces (facesum, face_data) VALUES (?,?)', (cache_key, pickle.dumps(faces)))
            self.cache_connection.commit()

        return faces


    def generate_frames_from_animation(self): 
        frames = []
        durations = []
        nframes = 0
        while self.image:
            try:
                self.image.seek( nframes )
                if ('duration' in self.image.info):
                    durations.append(int(round(self.image.info['duration'] / 10)))
                else:
                    durations.append(self.__class__.delay)
            except EOFError:
                break;
        
            # extract frame
            frame_image = self.image.convert('RGBA')
            frames.append(NamedTemporaryFile(suffix='.gif'))
            frame_image.save(frames[-1].name, 'GIF')
            with io.open(frames[-1].name, 'rb') as image_file:
                content = image_file.read()

            faces = self.transform_faces(self.get_faces(content))

            frame_image = self.manipulate_frame( frame_image, faces, nframes )
            self.raw_frames.append(frame_image)

            frames[-1] = NamedTemporaryFile(suffix='.gif')
            frame_image.save(frames[-1])
            nframes += 1

        return (frames, durations)

    def generate_frames_from_image(self): 

        frames = []
        durations = []
        for (i) in range(0, self.total_frames) if self.total_frames > 1 else [0]:
        
            faces = self.transform_faces(self.get_faces(self.imdata))

            out = self.manipulate_frame( self.image.copy(), faces, i )
            self.raw_frames.append(out)

            frames.append(NamedTemporaryFile(suffix='.gif'))
            durations.append(self.__class__.delay)
            out.save(frames[-1])

        return (frames, durations)

    def transform_faces(self, faces):
        return map(lambda face: Face.from_google_face(face), faces)

    def gif(self):
        try:
            outname = self.destdir + self.__class__.name + "/" + self.hash + ".gif"
            self.imdata = urllib.urlopen(self.url).read()
            self.image = Image.open(cStringIO.StringIO(self.imdata))
            if (len(self.secondary_urls) > 0):
                self.secondary_imdata = []
                self.secondary_image = []
                for url in self.secondary_urls:
                    imdata = urllib.urlopen(url).read();
                    self.secondary_imdata.append(imdata)
                    self.secondary_image.append(Image.open(cStringIO.StringIO(imdata)))

            self.animated_source = self.check_animated(self.image)

            durations = [self.__class__.delay]
            if (self.animated_source):
                self.total_frames = self.animated_source
                (frames, durations) = self.generate_frames_from_animation()
                cmd = "/usr/bin/gifsicle -l0 --colors 255"
            else:
                (frames, durations) = self.generate_frames_from_image()
                cmd = "/usr/bin/gifsicle --delay=" + str(self.__class__.delay) + " -l0 --colors 255"

            if (self.total_frames == 1 and not self.animated_source):
                outname = self.destdir + self.__class__.name + "/" + self.hash + ".jpg"
                self.raw_frames[-1].save(outname)
                return outname
            else:
                for x in xrange(0,self.total_frames):
                    cmd += ' -d' + str(durations[x]) + ' ' + frames[x].name

            cmd += " > " + outname

            call(cmd, shell=True)
            if (self.cache_connection):
                self.cache_connection.close()
            return outname
        except Exception as e:
            pprint.pprint(e)
            if (self.cache_connection):
                self.cache_connection.close()

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


