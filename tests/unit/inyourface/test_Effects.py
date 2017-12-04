from tests import *
import inyourface
import inspect, os
from inyourface.effect import *
from tests.helpers import *
import tests.helpers.AnimatorHelper

class TestEffects(unittest.TestCase):

    def test_effects(self):
            effects = inspect.getmembers(inyourface.effect, inspect.ismodule)
            for effect in effects:
                if (effect[0] == 'Swap'):
                    # this one has some extra args and should be tested on its own
                    continue
                animator = tests.helpers.AnimatorHelper.get_animator('sample_image_with_faces.jpg', False, effect[1].EffectAnimator)
                gif_path = animator.gif()
                self.assertTrue(os.path.isfile(gif_path), "Output is a file that exists")



