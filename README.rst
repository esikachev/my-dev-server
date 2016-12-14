My-dev server
=============
.. image:: https://travis-ci.org/esikachev/my-dev-server.svg?branch=master
    :target: https://travis-ci.org/esikachev/my-dev-server


**My-dev server information**

My-dev is an useful utility for developers. The aim of this project: provide
ability to use this repository like server for my-dev.


**Installation**

1. Create DB

- You can use any DB. (Tested on MySQL)
- Create DB named ``my_dev``

2. Modify db_url in config-file ``etc/my-dev-server/my-dev-server.conf``

3. Migrate DB via command:

.. sourcecode:: console

    $ tox -e venv -- my-dev-migrate --config-file etc/my-dev-server/my-dev-server.conf
..
