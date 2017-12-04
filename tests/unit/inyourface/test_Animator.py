from tests import *
import inyourface
import hashlib, pickle, mock, urllib, os, json, pprint, re, pkgutil, inspect
from inyourface.effect import *
from inyourface import Animator
from google.cloud import vision
from google.cloud.vision.annotations import Annotations
from tests.helpers import *
import tests.helpers.InMemoryCacheProvider
import tests.helpers.AnimatorHelper

class TestAnimator(unittest.TestCase):

    @mock.patch.object(vision, 'Client')
    @mock.patch.object(inyourface.DefaultCacheProvider, 'CacheProvider')
    def test_constructor(self, cache_provider, vision_client):
        animator = Animator(["url"], "/dev/null", None)
        vision_client.assert_called_once()
        cache_provider.assert_not_called()
        self.assertEqual("url", animator.url)
        self.assertEqual([], animator.secondary_urls)

        animator = Animator(["url","url2"], "/dev/null", None)
        cache_provider.assert_not_called()
        self.assertEqual(["url"], animator.secondary_urls)

        animator = Animator(["url","url2"], "/dev/null", "/dev/null")
        cache_provider.assert_called_once()
        self.assertEqual(["url"], animator.secondary_urls)

    def test_set_cache_provider(self):
        animator = tests.helpers.AnimatorHelper.get_animator()
        animator.set_cache_provider("Cats")
        self.assertEqual("Cats", animator.cache_provider)

    def test_get_faces(self):
        image_data = "image data"
        face_data = "Cats"

        hasher = hashlib.md5()
        hasher.update(image_data)
        cache_key = hasher.hexdigest()

        animator = tests.helpers.AnimatorHelper.get_animator('sample_image_with_faces.jpg', True)
        mock_image  = animator.vision_client.image.return_value
        mock_image.detect_faces.return_value = face_data
        animator.get_faces(image_data)
        animator.vision_client.image.assert_called_once()
        mock_image.detect_faces.assert_called_once()

        self.assertEqual(1, animator.cache_provider.get_calls[cache_key], "Checked cache")
        self.assertEqual(face_data, pickle.loads(animator.cache_provider.set_calls[cache_key]), "Cached result")

        animator.get_faces(image_data)
        self.assertEqual(2, animator.cache_provider.get_calls[cache_key], "Checked cache")
        # No additional call to image api on cache hit
        animator.vision_client.image.assert_called_once()


    def test_gif_on_jpg(self):
        animator = tests.helpers.AnimatorHelper.get_animator()
        gif_path = animator.gif()
        self.assertTrue(re.search('\.gif$', gif_path), "gif-looking file")
        self.assertTrue(os.path.isfile(gif_path), "Output is a file that exists")

    def test_gif_on_gif(self):
        animator = tests.helpers.AnimatorHelper.get_animator("sample_gif_with_faces.gif")
        gif_path = animator.gif()
        
        self.assertEqual(animator.total_frames, len(animator.cache_provider.get_calls), "Got face data for three frames in gif")
        self.assertTrue(re.search('\.gif$', gif_path), "gif-looking file")
        self.assertTrue(os.path.isfile(gif_path), "Output is a file that exists")

