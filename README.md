# sirius
shipping optimizer

## local installation
follow these instructions to get a local copy up and running

### virtualenv / pip
make sure you have `pip` installed on your system. if you don't, follow [these instructions](http://www.pip-installer.org/en/latest/installing.html).

make sure you have `virtualenv` installed on your system. if you don't, follow [these instructions](http://www.virtualenv.org/en/latest/virtualenv.html#installation).

after you have installed those, go to your source directory of choice and run the following:

```
$ virtualenv sirius-env
...
$ cd sirius-env
$ . bin/activate
```

the activation will prefix your shell with the environment's name.

### git clone repo
the next thing to do is to clone the repo with git. if you don't have git installed, kill yourself. seriously. what kind of dev are you?

```
$ git git@github.com:doggyloot/sirius.git
$ cd sirius
```

### install the dependencies
there are a number of environment-demanded requirements. for local purposes, use the dev stuff. install them with the following:

```
$ pip install -r reqs/dev.txt
```

### ensuring installation
the best way to find out that this went correctly is to run the local test server. do this:

```
$ ./manage.py runserver
...
```

and point your browser to [http://localhost:8000/](http://localhost:8000/). you should see the super simple, super ugly test page i made.

to kill the server, fire off a `ctrl+C` in the terminal.

## run the tests
to run the tests, make sure your environment is active (`. bin/activate`) and you're in the project directory (`/whatever/sirius-env/sirius/`).

the best way to run the tests is to fire off the following:

```
$ ./manage.py test
```

since this is a django project, it will run the full test suite on its own.

## deploying to heroku
heroku is a massive pain in the ass, despite what so many other people say. the best i found is to [follow this guy's approach](http://django-skel.readthedocs.org/en/latest/running-on-heroku/).

this project's structure is actually based on his template - again heroku + vince = disaster.
