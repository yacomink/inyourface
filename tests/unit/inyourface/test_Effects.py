from tests import *
import inyourface
import inspect, os, mock
from inyourface.effect import *
from tests.helpers import *
import tests.helpers.AnimatorHelper

class TestEffects(unittest.TestCase):

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, content):
                self.content = content

            def content():
                return self.content

        f = open("tests/data/sample_gif_with_faces.gif", "rb")
        return MockResponse(f.read())

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_effects(self, mockRequest):
            effects = inspect.getmembers(inyourface.effect, inspect.ismodule)
            for effect in effects:
                if (effect[0] == 'Swap'):
                    # this one has some extra args and should be tested on its own
                    continue
                animator = tests.helpers.AnimatorHelper.get_animator('sample_image_with_faces.jpg', False, effect[1].EffectAnimator)
                gif_path = animator.gif()
                self.assertTrue(os.path.isfile(gif_path), "Output is a file that exists")



