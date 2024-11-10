pip3 install --upgrade pip
pip3 install python-dotenv
pip3 install --upgrade pip setuptools wheel
pip3 install Cython
pip3 install "PyYAML==6.0" --only-binary :all:
pip3 install -r requirements.txt
python3 manage.py collectstatic