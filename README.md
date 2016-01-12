# stocker

``` console
# install virtualenv
$ sudo easy_install pip
$ sudo pip install virtualenv

# install project dependencies
$ ./build

# setup database
$ ./run python database.py

# populate companies in database
./run import_companies.py

# populate current finance data
./run import_financial_data.py yahoo_finance_quotes
./run import_financial_data.py yahoo_finance_ks
```
