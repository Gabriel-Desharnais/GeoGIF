#! /bin/bash

# Activate virtual env
source python3-env/bin/activate

# Start the test server
cd FrontEnd
python3 manage.py runserver 127.0.0.1

# Leave the virtual env
deactivate
