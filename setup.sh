#!/bin/bash


# PYTHON=python3-env

# virtualenv -p python3 ${PYTHON} --system-site-packages

# source ${PYTHON}/bin/activate

#mkdir package_download
#cd package_download
#apt-get download python3-dev
#apt-get download libpython3-dev
#apt-get download python3-imaging

#pip install -U pip
#pip install numpy
#pip install Pillow
#pip install moviepy
#pip install owslib
#pip install imageio
#pip install isodate
# pip install six
# pip install urllib3
# pip install chardet
# pip install certifi
# pip install idna
# pip install django
# pip install oauth2
# pip install TwitterAPI
# pip install -U setuptools wheel
# pip install ruamel.yaml

# install ffmpeg
python3 -c "import imageio; imageio.plugins.ffmpeg.download()"

MY_PATH="`dirname \"$0\"`"
cd "`( cd \"$MY_PATH\" && pwd )`"

GGcontroller/updateStatic.sh
GGcontroller/updateDB.sh
# deactivate
