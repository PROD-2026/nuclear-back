#!/bin/sh

exec celery -A src.celery_app worker --loglevel=info
