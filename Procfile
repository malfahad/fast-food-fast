web: TEST_DATABASE_URL=$(heroku config:get DATABASE_URL -a andelafastfoodfast) PRODUCTION_DATABASE_URL=$(heroku config:get DATABASE_URL -a myfastfoodfast) gunicorn -w 1 app:app
