# db_connect_mag

Utilities to connect to custom MySQL (local) database for Microsoft Academic Graph data.

Before importing, environment variables must be set:

```
MYSQL_USERNAME="myusername"
MYSQL_PASSWORD="mypassword"
MYSQL_DB_NAME="dbname"
```

One way to set these is to use the `python-dotenv` library (`pip install python-dotenv`) and load the variables from a `.env` file (which you do not commit to version control):

```
from dotenv import load_dotenv
load_dotenv('.env')
```
