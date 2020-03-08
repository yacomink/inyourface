from tests import *
import inyourface
import hashlib, pickle, mock, urllib.request, urllib.parse, urllib.error, os, json, pprint, re, pkgutil, inspect
from inyourface.effect import *
from inyourface import Animator
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf import message as _message
from tests.helpers import *
import tests.helpers.InMemoryCacheProvider

class MinimalAnimator(Animator):
    frames = list(range(0,2))
    def manipulate_frame(self, frame_image, faces, index):
        return frame_image


def getPathForTestDataFile(path):
    return os.path.dirname(os.path.realpath(__file__)) + "/../data/" + path

def get_sample_data(image):
    file_path = getPathForTestDataFile( re.sub('(jpg|gif)$', 'protobuf', image ) )
    with open(file_path, 'rb') as f:
        data = f.read()
        f.close()
        return string_to_face(data)


def get_animator(image='sample_image_with_faces.jpg', cache=False, animator_class=MinimalAnimator):
    with mock.patch.object(vision, 'ImageAnnotatorClient') as vision_client:
        cacher = tests.helpers.InMemoryCacheProvider.CacheProviderForTests(cache)
        animator = animator_class([getPathForTestDataFile( image )], None, None)
        animator.set_cache_provider(cacher)
        mock_image = animator.vision_client.face_detection.return_value
        mock_image.face_annotations.return_value = get_sample_data(image)
        return animator

def string_to_face(data):
    cached_faces = types.AnnotateImageResponse()
    cached_faces.ParseFromString(data)
    return cached_faces.face_annotations


