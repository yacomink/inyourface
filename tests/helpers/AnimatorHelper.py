from tests import *
import inyourface
import hashlib, pickle, mock, urllib, os, json, pprint, re, pkgutil, inspect
from inyourface.effect import *
from inyourface import Animator
from google.cloud import vision
from google.cloud.vision.annotations import Annotations
from tests.helpers import *
import tests.helpers.InMemoryCacheProvider

class MinimalAnimator(Animator):
    frames = range(0,2)
    def manipulate_frame(self, frame_image, faces, index):
        return frame_image


def getPathForTestDataFile(path):
    return os.path.dirname(os.path.realpath(__file__)) + "/../data/" + path

def get_sample_data(image):
    file_path = getPathForTestDataFile( re.sub('(jpg|gif)$', 'json', image ) )
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
        return Annotations.from_api_repr(data.get('responses')[0]).faces

def get_animator(image='sample_image_with_faces.jpg', cache=False, animator_class=MinimalAnimator):
    with mock.patch.object(vision, 'Client') as vision_client:
        cacher = tests.helpers.InMemoryCacheProvider.CacheProviderForTests(cache)
        animator = animator_class([getPathForTestDataFile( image )], None, None)
        animator.set_cache_provider(cacher)
        mock_image  = animator.vision_client.image.return_value
        mock_image.detect_faces.return_value = get_sample_data(image)
        return animator

