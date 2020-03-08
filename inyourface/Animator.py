import sys, logging, io, hashlib, pprint, io, os, pickle, inspect, traceback
from six.moves import urllib
from subprocess import call
from PIL import Image, ImageDraw
from tempfile import NamedTemporaryFile

from inyourface.Face import Face
from google.cloud import vision
from google.cloud.vision import types, enums
import inyourface.DefaultCacheProvider

class Animator(object):
    
    frames = list(range(0,9))
    name = "base"
    delay = 24

    def __init__(self, url, destdir, cache_dir):
        self.vision_client = vision.ImageAnnotatorClient()
        self.url = url[-1]
        if len(url) > 1:
            self.secondary_urls = list(url[0:-1])
        else:
            self.secondary_urls = []
        self.destdir = destdir
        self.cache_dir = cache_dir
        self.cache_provider = False
        self.raw_frames = []
        self.total_frames = len(self.__class__.frames)

        hasher = hashlib.sha1()
        hasher.update(self.__class__.name.encode('utf-8'))
        hasher.update(','.join(url).encode('utf-8'))

        if (self.cache_dir):
            self.cache_provider = inyourface.DefaultCacheProvider.CacheProvider(self.cache_dir)

        self.hash = hasher.hexdigest()

    def manipulate_frame(self, frame_image, faces, index):
        raise NotImplementedError( "Should have implemented this" )

    def set_cache_provider(self, provider):
        self.cache_provider = provider

    def get_faces(self, image_data):

        cache_key = self.get_cache_key_for_image(image_data)
        if (self.cache_provider):
            res = self.cache_provider.get(cache_key)
            if (res):
                print(res)
                cached_faces = types.AnnotateImageResponse()
                cached_faces.ParseFromString(res)
                return cached_faces.face_annotations

        image = types.Image(content=image_data)
        response = self.vision_client.face_detection(image=image)
        faces = response.face_annotations

        if (self.cache_provider):
            self.cache_provider.set(cache_key, response.SerializeToString())

        return faces

    def get_cache_key_for_image(self, image_data):
        hasher = hashlib.md5()
        hasher.update(image_data)
        hasher.update('protobuf'.encode('utf-8'))
        return hasher.hexdigest()

    def __generate_frames_from_animation(self): 
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

            faces = self.__transform_faces(self.get_faces(content))

            try:
                frame_image = self.manipulate_frame( frame_image, faces, nframes )
            except:
                logging.exception("Something awful happened!")

            self.raw_frames.append(frame_image)

            frames[-1] = NamedTemporaryFile(suffix='.gif')
            frame_image.save(frames[-1])
            nframes += 1

        return (frames, durations)

    def __generate_frames_from_image(self): 

        frames = []
        durations = []
        for (i) in list(range(0, self.total_frames)) if self.total_frames > 1 else [0]:
        
            faces = self.__transform_faces(self.get_faces(self.imdata))

            try:
                out = self.manipulate_frame( self.image.copy(), faces, i )
                self.raw_frames.append(out)

                frames.append(NamedTemporaryFile(suffix='.gif'))
                durations.append(self.__class__.delay)
                out.save(frames[-1])
            except:
                logging.exception("Something awful happened!")
    
        return (frames, durations)

    def __transform_faces(self, faces):
        return [Face(face) for face in faces]

    def gif(self):
        try:
            if (self.destdir):
                outname = self.destdir + self.hash + ".gif"
            else:
                outname = NamedTemporaryFile(suffix='.{}.gif'.format(self.hash)).name
            self.imdata = urllib.request.urlopen(self.url).read()
            self.image = Image.open(io.BytesIO(self.imdata))
            self.secondary_imdata = []
            self.secondary_image = []
            if (len(self.secondary_urls) > 0):
                for url in self.secondary_urls:
                    imdata = urllib.request.urlopen(url).read();
                    self.secondary_imdata.append(imdata)
                    self.secondary_image.append(Image.open(io.StringIO(imdata)))

            self.animated_source = self.check_animated(self.image)

            durations = [self.__class__.delay]
            if (self.animated_source):
                self.total_frames = self.animated_source
                (frames, durations) = self.__generate_frames_from_animation()
                cmd = "gifsicle --no-warnings -l0 --colors 255"
            else:
                (frames, durations) = self.__generate_frames_from_image()
                cmd = "gifsicle --no-warnings --delay=" + str(self.__class__.delay) + " -l0 --colors 255"

            if (self.total_frames == 1 and not self.animated_source):
                if (self.destdir):
                    outname = self.destdir + self.hash + ".jpg"
                else:
                    outname = NamedTemporaryFile(suffix='.{}.jpg'.format(self.hash)).name
                self.raw_frames[-1].save(outname)
                return outname
            else:
                for x in range(0,self.total_frames):
                    cmd += ' -d' + str(durations[x]) + ' ' + frames[x].name

            cmd += " > " + outname

            call(cmd, shell=True)
            if (self.cache_provider):
                self.cache_provider.close()
            return outname
        except Exception as e:
            pprint.pprint(e)
            if (self.cache_provider):
                self.cache_provider.close()
            traceback.print_exc()

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

    @staticmethod
    def get_os_path(directory=""):
        dir_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return dir_path + "/" + directory
