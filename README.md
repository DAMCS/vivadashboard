# VMS
A simple dashboard for viva management.

## Features
* Made using the [Django] framework.
* Currently deployed on [WSGI] for development.
* [Bootstrap] framework for responsive webpages.
* [AJAX] handles asynchronous calls.
* Uses [google forms] to collect application data from users.
* Retrieves application data using the [gspread] python API, authenticated by the [oauth2client] python library.
* Location parsing done by the [PhantomJS] driver to convert URL to GPS coordinates.
* Design and rendering of charts using [Chart.js].
* [Vue] for easy UI handling.
* Simple notifications done through [toastr].
* Custom scrollbar using the [jQuery] plugin [mcustomscrollbar] and many other plugins such as [hoverintent], [jb.flipText] and [mb.Extruder].
* [Materialize] for incorporating material design.
* Rich Configuration through custom utilities.
* Usage of fonts like [Cabin] and [roboto], including SVG icon fonts such as [font-awesome] and [icomoon].
* [SQLite] as an embedded SQL database engine.

## Development
Create the virtual environment on [Python] 3.7+
```sh
$ python -m venv /path/to/new/virtual/environment
```
Upgrade pip!
```sh
$ python -m pip install --upgrade pip
```
Clone this repository ;)
```sh
$ git clone https://github.com/DAMCS/vivadashboard.git
```
Install requirements.txt
```sh
$ cd /path/to/repository
$ python -m pip install -r requirements.txt
```
Refactor secret files not under source control and run the development server.
```sh
$ python manage.py runserver
```

## Requirements
* [requests]==2.19.1
* [Django]==2.1.2
* [pandas]==0.23.4
* [gspread]==3.0.1
* [Pillow]==5.2.0
* [google_api_python_client]==1.7.4
* [django-extensions]==2.1.2

[//]: # (Comments)

[Django]: <https://github.com/django/django>
[jQuery]: <https://jquery.com/>
[Bootstrap]: <>
[AJAX]: <https://code.djangoproject.com/wiki/AJAX>
[gspread]: <https://github.com/burnash/gspread>
[google forms]: <https://www.google.com/forms/about/>
[oauth2client]: <https://github.com/googleapis/oauth2client>
[WSGI]: <https://wsgi.readthedocs.io/en/latest/#>
[PhantomJS]: <https://github.com/ariya/phantomjs/>
[Chart.js]: <https://github.com/chartjs/Chart.js>
[Vue]: <https://github.com/vuejs/vue>
[mcustomscrollbar]: <https://github.com/malihu/malihu-custom-scrollbar-plugin>
[Materialize]: <https://github.com/dogfalo/materialize/>
[toastr]: <https://github.com/CodeSeven/toastr>
[requests]: <https://github.com/requests/requests/>
[pandas]: <https://github.com/pandas-dev/pandas>
[Pillow]: <https://github.com/python-pillow/Pillow>
[google_api_python_client]: <https://github.com/googleapis/google-api-python-client>
[django-extensions]: <https://github.com/django-extensions/django-extensions>
[Cabin]: <https://fonts.google.com/specimen/Cabin>
[font-awesome]: <https://github.com/FortAwesome/Font-Awesome>
[roboto]: <https://fonts.google.com/specimen/Roboto>
[icomoon]: <https://icomoon.io/>
[SQLite]: <https://sqlite.org/index.html>
[Python]: <https://github.com/python/cpython>
[hoverintent]: <https://github.com/briancherne/jquery-hoverIntent>
[jb.flipText]: <https://github.com/pupunzi/jquery.mb.flipText>
[mb.Extruder]: <https://github.com/pupunzi/jquery.mb.extruder>
