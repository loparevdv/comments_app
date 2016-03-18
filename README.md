# comments_app

Clojure Table + Adjacency List mix schema used.
Through some disk overhead this schema allows perform main (CRUD and get branch) operations extremely quick.

Clojure Table consistency provided by database trigger. 

postgresql should be used.



1. install dependencies ```pip install -r pip req```
2. init database using ```utils/db_init.sql``` script
3. run app 
```
gunicorn server:app --worker-class aiohttp.worker.GunicornWebWorker -b localhost:8080 -w 8
```
4. run loading script ```sh utils/load.sh```
5. feel free to check api (server.py)


Tech debts

1. override default 500 handler
2. unittests (or may be functional via curl)
3. check for database keys, indexes etc
4. incode TODOs

TODO:

1. pubsub interface
