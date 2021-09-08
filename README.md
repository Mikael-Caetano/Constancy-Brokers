# Constancy Brokers
A simple trading api.

## How to install and run:  
Pre-requisites:  
  Docker/Docker Desktop installed and running.  
  
1. Open your command prompt, then create or open the folder where you want to clone the repo:
```
cd path/to/your/dev/folder/
mkdir constancy_brokers
cd constancy_brokers
```
2. Clone this repository, it will download all the necessary files to you run this project in your localhost:
```
git clone https://github.com/Mikael-Caetano/Constancy-Brokers .
```

3. Navigate to constancy_brokers:
```
cd constancy_brokers
```

4. Run the `docker-compose up` command:
```
docker-compose up
```
If you get an "standard_init_linux.go:211: exec user process caused "no such file or directory" error:
Checkout that the "End of line sequence" setting of the file docker-entrypoint.sh is LF, otherwise change it to LF.

5. Open your browser and go to 127.0.0.1:8000 or localhost, the application should be running. If you want to test the API you can use the Browsable API, to do that you can follow the API urls listed below.

6. For the sake of testing the API, you must create a superuser, to do that you can run or add the following command to the file docker-entrypoint.sh:
```
python manage.py createsuperuser --username example --password example --email example@example.com --first_name example --last_name example --is_provider_admin True --noinput
```
You can set all the example data to your preferences.

7. (optional) In case you use postman, import the file Trade.postman_collection.json and User.postman_collection.json in your Postman software, it will help you test the application easily.


# API documentation:
## api/user/register/
* POST - Register a new user - arguments: username, password, first_name, last_name, email
```json
{
    "username": "user_6",
    "password": "password",
    "first_name": "User",
    "last_name": "6",
    "email": "email@email.com"
}
```

## api/user/login/
* POST - Login in user account - arguments: username, password
```json
{
    "username": "{{USERNAME}}",
    "password": "{{PASSWORD}}"
}
```

## api/trade/trades/
* POST - Create trade - arguments: provider, pair, quantity, price
```json
{
    "provider": 381,
    "pair": 1258,
    "quantity": 200,
    "price": 300.04
}
```

## api/trade/trades/(id)/
* PUT - Update trade - arguments: provider, pair, quantity, price
```json
{
    "provider": 381,
    "pair": 1258,
    "quantity": 200,
    "price": 300.04
}
```

## api/trade/providers/
* GET - List providers

* POST - Create provider - arguments: name, acronym
```json
{
    "name": "Test",
    "acronym": "TES"
}
```

## api/trade/providers/(id)/
* GET - Retrieve provider

* PUT - Update provider - arguments: name, acronym
```json
{
    "name": "edited test",
    "acronym": "ETS"
}
```

* DELETE - Delete provider

## api/trade/currencies/
* GET - List currencies

* POST - Create currency - arguments: name, acronym
```json
{
    "name": "Test",
    "acronym": "TES"
}
```

## api/trade/currencies/(id)/
* GET - Retrieve currency

* PUT - Update currency - arguments: name, acronym
```json
{
    "name": "edited test",
    "acronym": "ETS"
}
```

* DELETE - Delete currency

## api/trade/pairs/
* GET - List currency pairs

* POST - Create currency pair - arguments: from_currency, to_currency
```json
{
    "from_currency": 442,
    "to_currency": 446
}
```

## api/trade/pairs/(id)/
* GET - Retrieve currency pair

* PUT - Update currency pair - arguments: from_currency, to_currency
```json
{
    "from_currency": 442,
    "to_currency": 447
}
```

* DELETE - Delete currency pair

## api/trade/select-providers/
* GET - List providers for select
    * query arguments: page, search

## api/trade/select-currency-pairs/
* GET - List providers for select
    * query arguments: page, search

## api/trade/blotter/trades/
* List user trades
    * query arguments: pairs, min_price, max_price, min_quantity, max_quantity, start, end

## api/trade/blotter/trades/(id)
* GET - Retrieve trade data

## api/trade/blotter/trades/graph/
* GET - Retrieve user trades graph
    * query arguments: pairs, min_price, max_price, min_quantity, max_quantity, start, end

## api/trade/market/
* GET - Retrieve market graph
    * query arguments: pair, providers, start, end

    * overall - The average selling price among all brokers.
    * vwap - https://www.investopedia.com/terms/v/vwap.asp
    * feed - The selling price for the logged user.