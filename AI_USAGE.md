tools ->

    clade ai -> tool


prompts ->

hey i want to build ecommerce website
using django mysql and react js
here is the SRS 
We operate an ecommerce platform. When a customer places an order, the warehouse team needs to know which shipping box should be used. 
Each product has dimensions and weight. 
Each box has internal dimensions, maximum weight capacity, and cost.
Your task is to design and build a small Django-based system that recommends the most
suitable box for an order.



then i choose

Just build the box-recommendation module (the SRS task)


explore the whole project and files 
know how all the things work and flow


    then apply migrations
    db configurations
    run app 
    check all vsersion like mysql, django -> 6.1, python-> Python 3.13.0 suitable or not



github actions propmt

github action

run migration using sqlite


name: Django Tests
on:
  push:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - name: Install MySQL dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y default-libmysqlclient-dev build-essential pkg-config
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run migrations using SQLite
        run: |
          python manage.py migrate --settings=box_recommender.test_settings
      - name: Run tests using SQLite
        run: |
          python manage.py test --settings=box_recommender.test_settings -v 2


i have used sqlite 




then i done changes in the database in setting beacuse i uased django vsersion 6.1
for the mysql C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe  Ver 8.0.40 for Win64 on x86_64 (MySQL Community Server - GPL) vsersion was not supported

so then i switch to the SQLite



then add tests.yml file with the help of chatgpt

then i explore github actions and how it works



1. database 


if os.environ.get("DJANGO_TEST_MODE") == "1":
    # Self-contained, no external DB needed — used by `manage.py test`.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.environ.get("MYSQL_DATABASE", "box_recommender"),
                "USER": os.environ.get("MYSQL_USER", "root"),
                "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
                "HOST": os.environ.get("MYSQL_HOST", "127.0.0.1"),
                "PORT": os.environ.get("MYSQL_PORT", "3306"),
                "OPTIONS": {"charset": "utf8mb4"},
            }
    }


then switch to beause of django vsersion

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}



2. test database 

like name -> memory

python manage.py test -> create automatically db 


3. migrations-> 

python manage.py makemigrations

python manage.py migrate



4. test cases output in terminal / Django tests-> 

(venv) PS D:\box_recommender> python manage.py test     
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
D:\box_recommender\venv\Lib\site-packages\rest_framework\fields.py:1009: UserWarning: min_value should be an integer or Decimal instance.
  warnings.warn("min_value should be an integer or Decimalinstance.")
.......
----------------------------------------------------------------------
Ran 7 tests in 0.126s

OK
Destroying test database for alias 'default'...
(venv) PS D:\box_recommender> 



5. WSGI issue 

then run
then add


import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()


6. github actions

.github/workflow/tests.yml

name: Django Tests

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt


      - name: Run migrations
        run: |
          python manage.py migrate

      - name: Run tests
        run: |
          python manage.py test




6. commit changes 

git init
git add .
git commit -m 'msg'
git push




github action link -> 

https://github.com/aditigund2004/box_recommendation_ass/commit/0a07524b58e452be778b942a95534f6573615a5d