#!/bin/bash

# writing comments due to comment tree structure

curl --data "user_id=$1&parent_id=0&root_content_type=1&root_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=2&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=2&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=5&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=6&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=6&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=0&root_content_type=2&root_id=2&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=10&comment_text=11222" localhost:8080/create/
sleep .01
echo "10 done $1"
curl --data "user_id=$1&parent_id=11&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=10&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=12&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=12&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=14&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=9&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
echo "20 done $1"
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=16&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=20&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=19&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=24&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=25&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=25&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=25&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=25&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=27&comment_text=11222" localhost:8080/create/
sleep .01
echo "30 done $1"
curl --data "user_id=$1&parent_id=0&root_content_type=1&root_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=0&root_content_type=1&root_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=0&root_content_type=1&root_id=1&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=31&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=31&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=31&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=35&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=33&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=38&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=39&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=40&comment_text=11222" localhost:8080/create/
sleep .01
curl --data "user_id=$1&parent_id=40&comment_text=11222" localhost:8080/create/
sleep .01
echo "40 all done $1"