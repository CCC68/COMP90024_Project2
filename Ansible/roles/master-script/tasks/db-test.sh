#!/bin/bash
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'

docker create\
    -p 5984:5984\
    --name couchdb-test\
    --env COUCHDB_USER=${user}\
    --env COUCHDB_PASSWORD=${pass}\
    --env COUCHDB_SECRET=${cookie}\
    --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb-test\""\
    ibmcom/couchdb3:${VERSION}

docker start couchdb-test

curl http://127.0.0.1:5984