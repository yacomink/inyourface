import inspect, os
from inyourface.effect import Juggalo
from inyourface.Animator import Animator

class EffectAnimator(Juggalo.EffectAnimator):

    frames = [0]

    name = "clown"

    mask_path           = Animator.get_os_path("/overlays/mask.png")
    mask_elements_path  = Animator.get_os_path("/overlays/mask-elements.png")
    mask_mouth_path     = Animator.get_os_path("/overlays/mask-mouth.png")
