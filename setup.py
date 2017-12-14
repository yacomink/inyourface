import setuptools
from inyourface.version import Version


setuptools.setup(name='inyourface',
                 version=Version('0.0.1').number,
                 description='In Your Face',
                 long_description=open('README.md').read().strip(),
                 author='Andy Yaco-Mink (@yacomink), Samantha Goldstein (@goldsamantha)',
                 author_email='inyourface@yacomink.com',
                 url='https://github.com/yacomink/inyourface',
                 packages=['inyourface'],
                 package_data={'inyourface': ['overlays/*']},
                 scripts=['bin/inyourface'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='dumb gifs juggalos clowns',
                 classifiers=[])
