apt-get update && apt-get install -y python3.10 python3.10-dev python3.10-venv python3.10-distutils
python3.10 -m ensurepip --upgrade
python3.10 -m pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
