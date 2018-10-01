import subprocess

get_db_url_command = "DATABASE_URL=$(heroku config:get DATABASE_URL -a andelafastfoodfast)"
subprocess.call(get_db_url_command,shell=True)
