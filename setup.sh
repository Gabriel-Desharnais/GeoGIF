#!/bin/bash


PYTHON=python3-env

virtualenv -p python3 ${PYTHON}

source ${PYTHON}/bin/activate

mkdir package_download
cd package_download
apt-get download python3-dev
apt-get download libpython3-dev
apt-get download python3-imaging
dpkg -x python3-dev*.deb .
dpkg -x libpython3-dev*.deb .
dpkg -x python3-imaging*.dep .
cd ..
cp -R package_download/usr/bin python3-env/bin
cp -R package_download/usr/lib python3-env/lib


pip install numpy
pip install Pillow
pip install moviepy
pip install owslib
pip install imageio
pip install isodate
pip install six
pip install urllib3
pip install chardet
pip install certifi
pip install idna
pip install django
pip install oauth2
pip install TwitterAPI
pip install -U setuptools wheel
pip install ruamel.yaml

# install ffmpeg
python3 -c "import imageio; imageio.plugins.ffmpeg.download()"

GGcontroller/updateStatic.sh
GGcontroller/updateDB.sh
deactivate
