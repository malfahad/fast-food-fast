web: TEST_DATABASE_URL=$(heroku config:get DATABASE_URL -a myfastfoodfast) PDN_DATABASE_URL=$(heroku config:get DATABASE_URL -a andelafastfoodfast) gunicorn -w 1 app:app
