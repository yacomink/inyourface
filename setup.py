import setuptools
from inyourface.version import Version


setuptools.setup(name='inyourface',
                 version=Version('0.0.1').number,
                 description='In Your Face',
                 long_description=open('README.md').read().strip(),
                 author='Andy Yaco-Mink',
                 author_email='andy@yacomink.com',
                 url='https://github.com/yacomink/inyourface',
                 py_modules=['inyourface'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='dumb gifs juggalos clowns',
                 classifiers=[])
