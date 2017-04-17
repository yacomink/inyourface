import os
import sys
import click
import pprint
import inyourface.effect
from inyourface import EffectOrchestrator


import click
@click.command()
@click.option('--url', required=True, help='Url of the input image to be manipulated')
@click.option('--effect', '-e', required=True, multiple=True, help='The effect to apply, can specify multiple with -e effect1 -e effect2')

@click.option('--google_credentials', default='./google-credentials.json', help='Location of google API credentials json file.')
@click.option('--image_directory', default='./', help='Where to put finished images.')

# TODO: implement --list
#@click.option('--list', help='List available effects')

def run(url, effect, google_credentials, image_directory):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_credentials
    if (len(effect) == 0):
        print "You must specify some effects!"
        exit()
    elif (len(effect) == 1):
        effect_module = getattr(inyourface.effect, effect[0])
        gif = effect_module.EffectAnimator(url, image_directory)
        print gif.gif()
    else:
        gif = EffectOrchestrator(url, image_directory, effect)
        print gif.gif()

if __name__ == '__main__':
    run()
