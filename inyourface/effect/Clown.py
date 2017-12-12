import inspect, os
from inyourface.effect import Juggalo

class EffectAnimator(Juggalo.EffectAnimator):

    frames = [0]

    name = "clown"

    dir_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + "/../.."))

    mask_path           = dir_path + "/overlays/mask.png"
    mask_elements_path  = dir_path + "/overlays/mask-elements.png"
    mask_mouth_path     = dir_path + "/overlays/mask-mouth.png"
