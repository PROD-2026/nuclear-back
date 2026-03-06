#!/bin/sh

exec granian --interface asgi --host ${APP_HOST:=0.0.0.0} --port ${APP_PORT:=80} --workers ${APP_WORKERS:=1} --access-log --loop uvloop src.main:app 
