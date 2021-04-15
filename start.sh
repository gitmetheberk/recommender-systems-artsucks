#!/bin/bash

cd frontend

lcp --proxyUrl http://104.236.113.146:8000 > lcp.log&

echo LCP started

nohup npm start > frontend.log&

echo Frontend started

cd ..

cd backend

nohup pipenv run python manage.py runserver 0.0.0.0:8000 > backend.log&

echo Backend started

cd ..
