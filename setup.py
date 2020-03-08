import setuptools
from inyourface.version import Version

REQUIREMENTS = [
    "click",
    "opencv_python==4.2.0.32",
    "Pillow==6.2.0",
    "numpy>=1.12.0",
    "google-cloud-vision>=0.30.0",
    "google-cloud-storage>=1.8.0",
    "sympy",
    "six"
]

setuptools.setup(name='inyourface',
                 version=Version('0.0.14').number,
                 description='In Your Face',
                 long_description=open('README.rst').read().strip(),
                 author='Andy Yaco-Mink (@yacomink), Samantha Goldstein (@goldsamantha)',
                 author_email='inyourface@yacomink.com',
                 url='https://github.com/yacomink/inyourface',
                 packages=['inyourface','inyourface.effect'],
                 package_data={'inyourface': ['overlays/*']},
                 scripts=['bin/inyourface'],
                 install_requires=REQUIREMENTS,
                 license='MIT License',
                 zip_safe=False,
                 keywords='dumb gifs juggalos clowns',
                 classifiers=[])
