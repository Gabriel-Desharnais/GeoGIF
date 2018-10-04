#! /bin/bash

# Activate virtual env
source python3-env/bin/activate

# Collect static file in the static folders
cd FrontEnd
python3 manage.py collectstatic

# Leave the virtual env
deactivate
