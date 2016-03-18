# comments_app

clojure table + adjacency list mix schema used.
through disk overhead this schema allows perform main (CRUD and get branch) operations extremely quick.

clojure table consistency provided by database trigger

1. install dependencies ```pip install -r pip req```
2. run app ```gunicorn server:app --worker-class aiohttp.worker.GunicornWebWorker -b localhost:8080 -w 4```
3. run loading script ```sh utils/load.sh```
4. feel free to check api (server.py)
