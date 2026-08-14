(venv) PS D:\box_recommender> python manage.py migrate
Traceback (most recent call last):
  File "D:\box_recommender\manage.py", line 20, in <module>
    main()
    ~~~~^^
  File "D:\box_recommender\manage.py", line 16, in main
    execute_from_command_line(sys.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\__init__.py", line 443, in execute_from_command_line
    utility.execute()
    ~~~~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\__init__.py", line 437, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\base.py", line 422, in run_from_argv
    self.execute(*args, **cmd_options)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\base.py", line 466, in execute
    output = self.handle(*args, **options)
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\base.py", line 113, in wrapper
    res = handle_func(*args, **kwargs)
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\commands\migrate.py", line 115, in handle
    executor = MigrationExecutor(connection, self.migration_progress_callback)
  File "D:\box_recommender\venv\Lib\site-packages\django\db\migrations\executor.py", line 18, in __init__
    self.loader = MigrationLoader(self.connection)
                  ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\db\migrations\loader.py", line 59, in __init__
    self.build_graph()
    ~~~~~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\db\migrations\loader.py", line 288, in build_graph
    self.applied_migrations = recorder.applied_migrations()
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\db\migrations\recorder.py", line 89, in applied_migrations
    if self.has_table():
       ~~~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\db\migrations\recorder.py", line 63, in has_table
    with self.connection.cursor() as cursor:
         ~~~~~~~~~~~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\asyncio.py", line 26, in inner
    return func(*args, **kwargs)
  File "D:\box_recommender\venv\Lib\site-packages\django\db\backends\base\base.py", line 320, in cursor
    return self._cursor()
           ~~~~~~~~~~~~^^
  File "D:\box_recommender\venv\Lib\site-packages\django\db\backends\dummy\base.py", line 21, in complain
    raise ImproperlyConfigured(
    ...<3 lines>...
    )
django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured. Please supply the ENGINE value. Check settings documentation for more details.
(venv) PS D:\box_recommender> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, boxing, contenttypes, sessions
Running migrations:
  No migrations to apply.
(venv) PS D:\box_recommender> python manage.py test
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
D:\box_recommender\venv\Lib\site-packages\rest_framework\fields.py:1009: UserWarning: min_value should be an integer or Decimal instance.
  warnings.warn("min_value should be an integer or Decimal instance.")
.......
----------------------------------------------------------------------
Ran 7 tests in 0.065s

OK
Destroying test database for alias 'default'...
(venv) PS D:\box_recommender> python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Exception in thread django-main-thread:
Traceback (most recent call last):
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\module_loading.py", line 30, in import_string
    return cached_import(module_path, class_name)
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\module_loading.py", line 16, in cached_import
    return getattr(module, class_name)
AttributeError: module 'config.wsgi' has no attribute 'application'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\box_recommender\venv\Lib\site-packages\django\core\servers\basehttp.py", line 49, in get_internal_wsgi_application
    return import_string(app_path)
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\module_loading.py", line 32, in import_string
    raise ImportError(
    ...<2 lines>...
    ) from err
ImportError: Module "config.wsgi" does not define a "application" attribute/class

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Program Files\Python313\Lib\threading.py", line 1041, in _bootstrap_inner
    self.run()
    ~~~~~~~~^^
  File "C:\Program Files\Python313\Lib\threading.py", line 992, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\autoreload.py", line 83, in wrapper
    raise e
  File "D:\box_recommender\venv\Lib\site-packages\django\utils\autoreload.py", line 66, in wrapper
    fn(*args, **kwargs)
    ~~^^^^^^^^^^^^^^^^^
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\commands\runserver.py", line 143, in inner_run
    handler = self.get_handler(*args, **options)
  File "D:\box_recommender\venv\Lib\site-packages\django\contrib\staticfiles\management\commands\runserver.py", line 31, in get_handler
    handler = super().get_handler(*args, **options)
  File "D:\box_recommender\venv\Lib\site-packages\django\core\management\commands\runserver.py", line 73, in get_handler
    return get_internal_wsgi_application()
  File "D:\box_recommender\venv\Lib\site-packages\django\core\servers\basehttp.py", line 51, in get_internal_wsgi_application
    raise ImproperlyConfigured(
    ...<2 lines>...
    ) from err
django.core.exceptions.ImproperlyConfigured: WSGI application 'config.wsgi.application' could not be loaded; Error importing module.
D:\box_recommender\config\wsgi.py changed, reloading.
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 14, 2026 - 09:04:57
Django version 6.1, using settings 'config.settings'
Starting WSGI development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/6.1/howto/deployment/
Not Found: /
[14/Aug/2026 09:05:04] "GET / HTTP/1.1" 404 2376
Not Found: /favicon.ico
[14/Aug/2026 09:05:04] "GET /favicon.ico HTTP/1.1" 404 2427
[14/Aug/2026 09:05:10] "GET /api/ HTTP/1.1" 200 138
(venv) PS D:\box_recommender> python -m django --version                                                                                           
6.1
(venv) PS D:\box_recommender> mysql --version                                                                                                      
C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe  Ver 8.0.40 for Win64 on x86_64 (MySQL Community Server - GPL)
(venv) PS D:\box_recommender> python --version                                                                                                     
Python 3.13.0
(venv) PS D:\box_recommender> python manage.py test     
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
D:\box_recommender\venv\Lib\site-packages\rest_framework\fields.py:1009: UserWarning: min_value should be an integer or Decimal instance.
  warnings.warn("min_value should be an integer or Decimal instance.")
.......
----------------------------------------------------------------------
Ran 7 tests in 0.126s

OK
Destroying test database for alias 'default'...
(venv) PS D:\box_recommender> 






git bash


aditi@Aditi MINGW64 /d/box_recommender (main)
$  source /d/box_recommender/venv/Scripts/activate
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git init
Reinitialized existing Git repository in D:/box_recommender/.git/
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git commit -m 'changes in test_setting.py and setting.py file'
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   config/__pycache__/test_settings.cpython-313.pyc
        modified:   config/__pycache__/wsgi.cpython-313.pyc
        modified:   config/settings.py
        modified:   config/test_settings.py
        modified:   config/wsgi.py

no changes added to commit (use "git add" and/or "git commit -a")
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git status
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   config/__pycache__/test_settings.cpython-313.pyc
        modified:   config/__pycache__/wsgi.cpython-313.pyc
        modified:   config/settings.py
        modified:   config/test_settings.py
        modified:   config/wsgi.py

no changes added to commit (use "git add" and/or "git commit -a")
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git add .
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git push
Everything up-to-date
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git commit -m 'changes in test_setting.py and setting.py file'
[main 943fbf0] changes in test_setting.py and setting.py file
 5 files changed, 10 insertions(+), 12 deletions(-)
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git push
Enumerating objects: 14, done.
Counting objects: 100% (14/14), done.
Delta compression using up to 12 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 973 bytes | 162.00 KiB/s, done.
Total 8 (delta 5), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
To https://github.com/aditigund2004/box_recommendation_ass.git
   f14824a..943fbf0  main -> main
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ 
$ git add .
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git commit -m 'changes in tests.yml file'
[main 2d9f159] changes in tests.yml file
 1 file changed, 5 insertions(+), 9 deletions(-)
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git push
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 12 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (5/5), 423 bytes | 105.00 KiB/s, done.
Total 5 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
To https://github.com/aditigund2004/box_recommendation_ass.git
   943fbf0..2d9f159  main -> main
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git commit -m 'apply minimal chnages'
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   config/__pycache__/settings.cpython-313.pyc
        modified:   config/__pycache__/test_settings.cpython-313.pyc
        modified:   config/__pycache__/wsgi.cpython-313.pyc
        modified:   config/settings.py
        modified:   config/wsgi.py

no changes added to commit (use "git add" and/or "git commit -a")
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git push
Everything up-to-date
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git add .
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git commit -m 'apply minimal chnages'
[main 0a07524] apply minimal chnages
 5 files changed, 34 insertions(+), 19 deletions(-)
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ git push
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 12 threads
Compressing objects: 100% (9/9), done.
Writing objects: 100% (9/9), 1.58 KiB | 77.00 KiB/s, done.
Total 9 (delta 5), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
To https://github.com/aditigund2004/box_recommendation_ass.git
   2d9f159..0a07524  main -> main
(venv) 
aditi@Aditi MINGW64 /d/box_recommender (main)
$ 

