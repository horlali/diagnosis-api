python manage.py makemigrations
python manage.py migrate
python manage.py flush --no-input
python manage.py loaddata category
python manage.py loaddata diagnosis
python manage.py runserver
