# comments_app

clojure table + adjacency list mix schema used.
through disk overhead this schema allows perform main (CRUD and get branch) operations extremely quick.

clojure table consistency provided by database trigger

1. install dependencies ```pip install -r pip req```
2. init bd using ```utils/db_init.sql``` script
3. run app ```gunicorn server:app --worker-class aiohttp.worker.GunicornWebWorker -b localhost:8080 -w 4```
4. run loading script ```sh utils/load.sh```
5. feel free to check api (server.py)


Tech debts

1. override default 500 handler
2. unittests (or maybe via curl)
3. check for database keys, indexes etc

TODO:

1. reporting storage
2. pubsub interface