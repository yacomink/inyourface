import os 
from inyourface.effect import Juggalo

class EffectAnimator(Juggalo.EffectAnimator):

    frames = [0]

    name = "clown"

    mask_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask.png"
    mask_elements_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask-elements.png"
    mask_mouth_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask-mouth.png"
