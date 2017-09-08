FROM gcr.io/google-appengine/python

RUN apt-get update -y \
  && apt-get install -y gifsicle

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ENV FLASK_APP=server.py

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add the application source code.
ADD . /app

CMD gunicorn -b :$PORT server:app