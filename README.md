# bh-aust-postcode

A single endpoint web API to search for Australian postcodes based on locality aka suburb.

## Australian Postcodes Source

```
https://www.matthewproctor.com/Content/postcodes/australian_postcodes.json
```

This web API uses only ``locality``, ``state`` and ``postcode`` fields.

## Stable Revision 

### Tag <code>v0.0.1</code> -- July 3rd, 2023

This revision uses SQLite database file. Clone with:

```
git clone -b v0.0.1 https://github.com/behai-nguyen/bh-aust-postcode.git
```

## Project Setup and Run the Development Web Server

### Windows 10 Setup

Project directory is ``F:\bh_aust_postcode\``.

Create the virtual environment venv:

```
F:\bh_aust_postcode>C:\PF\Python310\Scripts\virtualenv.exe venv
```

To activate virtual environment venv:

```
F:\bh_aust_postcode>venv\Scripts\activate
```

Editable install project:

```
(venv) F:\bh_aust_postcode>venv\Scripts\pip.exe install -e .
```

### Windows 10 Run the Development Web Server

Download postcodes and write to SQLite database file:

```
(venv) F:\bh_aust_postcode>venv\Scripts\flask.exe update-postcode
```

Run the development web server:

```
(venv) F:\bh_aust_postcode>venv\Scripts\flask.exe run
```

The Swagger UI URL on localhost:

```
http://localhost:5000/api/v0/ui
```

To search for postcodes whom locality contains the string ``spring``:

```
http://localhost:5000/api/v0/aust-postcode/spring
```

### Ubuntu 22.10 Setup

Project directory is ``/home/behai/webwork/bh_aust_postcode``:

```
behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ pwd
```

Output:

```
/home/behai/webwork/bh_aust_postcode
```

Create the virtual environment venv:

```
behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ virtualenv venv
```

To activate virtual environment venv:

```
behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ source venv/bin/activate
```

Editable install project:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/pip install -e .
```

Install ``gunicorn`` separately:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/pip install gunicorn
```

### Ubuntu 22.10 Run the Development Web Server

Download postcodes and write to SQLite database file:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/flask update-postcode
```

Run the web server via ``gunicorn``:

```
(venv) behai@HP-Pavilion-15:~/webwork/bh_aust_postcode$ venv/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
```

The Swagger UI URL, accessed from Windows 10:

```
http://hp-pavilion-15:5000/api/v0/ui
```

To search for postcodes whom locality contains the string ``spring``:

```
http://hp-pavilion-15:5000/api/v0/aust-postcode/spring
```

## .env File

There is nothing secured about this project 😂:

```
SECRET_KEY=">s3g;?uV^K=`!(3.#ms_cdfy<c4ty%"
FLASK_APP=app.py
FLASK_DEBUG=True
# SOURCE_POSTCODE_URL="https://www.matthewproctor.com/Content/postcodes/australian_postcodes.json"
SOURCE_POSTCODE_URL="http://localhost/work/australian_postcodes.json"
SCHEMA="schema.sql"
DATABASE="australian_postcode.db"
```

## License

[ MIT license ](https://github.com/behai-nguyen/bh-aust-postcode/blob/main/LICENSE)

## jQuery plugin: bhAustPostcode

A jQuery plugin which enables searching for Australian postcodes based on locality aka suburb.

Repo: https://github.com/behai-nguyen/bh-aust-postcode/tree/main/jquery-bhaustpostcode
