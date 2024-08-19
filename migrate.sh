#/bin/sh
python3 manage.py makemigrations --force-color --no-input 
python3 manage.py makemigrations --merge --no-input
python3 manage.py makemigrations --force-color --no-input Account
python3 manage.py makemigrations --force-color --no-input Rss
python3 manage.py makemigrations --force-color --no-input Web
python3 manage.py migrate --force-color
python3 manage.py collectstatic --no-input --clear
python3 manage.py createsuperuser --noinput; exit 0