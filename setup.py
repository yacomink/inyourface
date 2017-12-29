import setuptools
from inyourface.version import Version

REQUIREMENTS = [
    "click==6.7",
    "opencv_python==3.2.0.6",
    "numpy==1.12.0",
    "Pillow==4.1.0",
    "google-cloud-vision==0.28.0",
    "google-cloud-storage==1.6.0",
    "sympy"
]

setuptools.setup(name='inyourface',
                 version=Version('0.0.11').number,
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
