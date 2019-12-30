========
Friendly
========

Friendly is an app which makes it easier to meet new people with similar
interests at conferences.

The story
---------

It was the afternoon of the final day of 36C3.

As we sat around enjoying the last hours of the event and watching the crowds
slowly thinning out, we started to reflect on the fact that it's often
difficult to meet new people at conferences.

And we thought "What if we made an app to help people meet new people at
conferences?".

So we found a table in what was left on the Python assembly, sat down, and
started building one.

Setting up a development instance
---------------------------------

These steps are for Debian and Debian derivatives.

They assume that your Python3 version is at least 3.6.

Step 1 - Install pip, virtualenv and virtualenvwrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can skip this step if you already have these installed.

Install pip::

    $ sudo apt update
    $ sudo apt install python-pip

Install virtualenv and virtualenvwrapper::

    $ pip install --user virtualenv virtualenvwrapper

Add these lines to the end of your ``~/.bashrc`` file::

    export WORKON_HOME="${HOME}/.virtualenvs"
    source ~/.local/bin/virtualenvwrapper.sh

Reload ``~/.bashrc``::

    $ source ~/.bashrc

Step 2 - Set up a virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set up a virtualenv called ``friendly``::

    $ mkvirtualenv --python=`which python3` friendly

Step 3 - Clone the repo
~~~~~~~~~~~~~~~~~~~~~~~

Clone the repo::

    $ cd /path/to/your/projects/directory
    $ git clone git@github.com:red-and-black/friendly.git

Step 4 - Install dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the required Python packages in your virtualenv::

    $ cd friendly
    $ pip install -r requirements.txt

Step 5 - Initialise a database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialise a database with::

    $ ./manage.py migrate

Step 6 - Create a superuser
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a superuser with::

    $ ./manage.py createsuperuser

Step 7 - Start the server
~~~~~~~~~~~~~~~~~~~~~~~~~

Start the server with::

    $ ./manage.py runserver

Step 8 - Access the app
~~~~~~~~~~~~~~~~~~~~~~~

Browse to http://localhost:8000.
