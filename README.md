# flask-forum
A customized online forum (simulation on local 8001 port) constructed by Python Flask and the MySQL.  A user is able to login/ logout, post/view questions raised by other users and comment or like the posts. Note that data in the MySQL is omitted since it can be given in any desired content. 



## Run

Download the code and run the content in app.py. Open http://127.0.0.1:8001/  in your favorite browser to see what is going on.



## Implementation

- **Framework**

Based on Flask, the extra required dependencies:

- **Flask**

  -  Flask- WTF

    

- **MySQL**
  - Flask-SQLAlchemy
  - MySQLClient



- **Others**
  - Bootstrap
  - jQuery



-  **Database Design （ORM Model）**

For the ORM design, I used the tool called [pdman](http://www.pdman.cn/#/).  The ORM model for this website's database is shown below:

**Accounts Management:**

![Accounts](docs\accounts_db.jpg)

**Forum functions:**

![Forum](docs\qa_db.jpg)



Create an local MySQL database (using any tool, i.e. command line),  connect it and build the db model with SQLAlchemy.  See models.py for implementation.



- **Optimization (Blueprints)**

Here is just a simple example on how the  Blueprint optimization is implemented in Flask:

```python
#  after we have extract the common functions to different modules

# first we init a blueprint obj, this time we take users' 'accounts' as an example
accounts = Blueprint('accounts',__name__,template_folder='templates',static_folder='static')

# then register this blueprint for further optimization
from accounts.views import accounts
app.register_blueprint(accounts,url_prefix='/accounts')
```

The [reason](https://flask.palletsprojects.com/en/2.0.x/blueprints/) why I use Blueprints to build modular application.



##  Contribute

Fork the repository and make pull requests.



## Contact

[My contacts](https://linktr.ee/shuheng_mo)
