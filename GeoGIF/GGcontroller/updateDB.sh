#! /bin/bash

# Activate virtual env
source python3-env/bin/activate

# update database
cd FrontEnd

python3 manage.py makemigrations
python3 manage.py migrate

# Leave the virtual env
deactivate
