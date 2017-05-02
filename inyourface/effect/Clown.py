import random
import cv2
from PIL import Image,ImageDraw,ImageEnhance
from tempfile import NamedTemporaryFile
import math
import numpy as np
from pprint import pprint
import os 

from inyourface.Animator import Animator
from inyourface.effect import Juggalo

class EffectAnimator(Juggalo.EffectAnimator):

    name = "clown"

    mask_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask.png"
    mask_elements_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask-elements.png"
    mask_mouth_path = os.path.dirname(os.path.realpath(__file__)) + "/../../overlays/mask-mouth.png"
