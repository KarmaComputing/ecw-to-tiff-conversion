# ecw-to-tiff-conversion

## How to run it
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
gunicorn -w 4 -b '127.0.0.1:5000' --chdir 'src' 'app:app'
```
