# comments_app

clojure table + adjacency list mix schema used.
through disk overhead this schema allows perform main (CRUD and get branch) operations extremely quick.

gunicorn server:app --worker-class aiohttp.worker.GunicornWebWorker -b localhost:8080 -w 4
sh load.sh

