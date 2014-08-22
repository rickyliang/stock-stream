Stock Stream
============

A Python desktop application that pulls data from Yahoo Finance (through Yahoo Query Language (YQL)).
Data is stored in a database (new data overwrites the old) and is displayed in a window via PyQt.



Pre-Requisites
--------------
Please make sure that these are installed:
* Python 2.7.x
* Python virtualenv



Requirements
------------
* alembic
* requests



Setup
-----
1. Download and unzip the files into a folder.

2. **Ensure that pip is installed.** For Windows users, see [here](http://flask.pocoo.org/docs/installation/#pip-and-distribute-on-windows) for instructions.
    * If you will have multiple versions of Python, check out [how to install and configure](http://stackoverflow.com/questions/4583367/how-to-run-multiple-python-version-on-windows) and [how to use pip](http://stackoverflow.com/questions/2812520/pip-dealing-with-multiple-python-versions) with another version of Python.

3. **Ensure that the `virtualenv` module for Python is installed.** Type `pip freeze` into terminal and check if `virtualenv` is listed.
    * If it is, update it to the most recent version by typing `sudo pip install --upgrade virtualenv`.
    * If not, simply type into terminal `sudo pip install virtualenv` for Linux and OSX users, or `pip install virtualenv` for Windows users, `pip2.7 install virtualenv` if you have multiple versions.

4. **Create a virtual environment.** Type into terminal `virtualenv venv` without the brackets, `virtualenv --python=[path/to/python/python.exe] venv` if you have multiple versions.

5. **Activate the virtual environment.** For Linux users, type into terminal `. venv/bin/activate`. For Windows users, type `venv\Scripts\activate`.

6. **Retrieve all the requirements.** Run `pip install -e .` to automatically install the needed dependencies.

7. **Install PySide GUI.** Run `pip install --use-wheel -U pyside`.

8. **Initialize alembic.** Run `alembic init alembic` to initialize alembic.

9. **Create the database.** Run `python db_create.py` to create your database with the name specified in config.py.

10. **Start the server.** Run `python run.py` and enjoy.



Customization
-------------
If you change your database name, change sqlalchemy.url in alembic.ini to point to your database.