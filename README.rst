In Your Face
------------

A handful of low-rent animations layered atop all the faces in your
image. Uses Google Vision API for face/feature detection, and gifsicle
for makin’ gifs.

Usage
~~~~~

::

    Usage: inyourface [OPTIONS]

    Options:
      --url TEXT                 Url of the input image to be manipulated
                                 [required]
      -e, --effect TEXT          The effect to apply, can specify multiple with -e
                                 effect1 -e effect2  [required]
      --google_credentials TEXT  Location of google API credentials json file.
      --image_directory TEXT     Where to put finished images.
      --help                     Show this message and exit.

Effects
~~~~~~~

========  ========  ===========
Angry     Crying    Cryingblood
|image0|  |image1|  |image2|
Googly    Thinking  Juggalo
|image3|  |image4|  |image8|
========  ========  ===========


Effect Combinations
~~~~~~~~~~~~~~~~~~~

Angry + Googly + Cryingblood
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|image6|

Googly + Thinking on a gif
^^^^^^^^^^^^^^^^^^^^^^^^^^

|image7|

Requirements
~~~~~~~~~~~~

1. ``gifsicle`` https://www.lcdf.org/gifsicle/

2. An account setup with the Google Vision API, and your credentials
   file ``google-credentials.json`` file somewhere that ``inyourface``
   can get to it.

.. figure:: https://travis-ci.org/yacomink/inyourface.svg?branch=master
   :alt: build status

   build status

.. |image0| image:: https://github.com/yacomink/inyourface/blob/master/examples/63d1c91a84f90cbf3978a7c9936cc966876ab1a0.gif?raw=true
.. |image1| image:: https://github.com/yacomink/inyourface/blob/master/examples/dfa3376f7075094f951cfb808eb530bffde9f930.gif?raw=true
.. |image2| image:: https://github.com/yacomink/inyourface/blob/master/examples/c050d3929b14252276557d4d72ca395bf92f597d.gif?raw=true
.. |image3| image:: https://github.com/yacomink/inyourface/blob/master/examples/0500b8896bee27f4db798a1c1d9a0e1d1d9a0784.gif?raw=true
.. |image4| image:: https://github.com/yacomink/inyourface/blob/master/examples/0969445f8dcd57fde556b9a7fb0018c44dbb9c44.gif?raw=true
.. |image5| image:: https://github.com/yacomink/inyourface/blob/master/examples/0500b8896bee27f4db798a1c1d9a0e1d1d9a0784.gif?raw=true
.. |image6| image:: https://github.com/yacomink/inyourface/blob/master/examples/2fecff2f9f51066c704fdeb16298873825f29579.gif?raw=true
.. |image7| image:: https://github.com/yacomink/inyourface/blob/master/examples/c4a82e74e0c35c71414693446d1fe49ce4288585.gif?raw=true
.. |image8| image:: https://snaps.yacomink.com/m/Image_2017-12-14_11-21-10.png
