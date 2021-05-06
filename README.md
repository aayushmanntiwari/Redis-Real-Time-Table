# Redis-Real-Time-Table
This app will automatically download the zip file from and extract it and update the csv data in the database using redis everyday at 6:00 p.m


Steps : 1.Clone this repo in your virtual env and activite the virutal env before runing any command. 
2.Run pip install -r requirements.txt cmd in the terminal to install dependency.
3.Install redis from here https://github.com/microsoftarchive/redis/releases and make sure to start the service. 
4.Run celery -A Main beat -l info and celery -A Main worker -l INFO to schedule the task if in locallost no need to run it in development 
i.e heroku as all settings are done for that . 
5.Enjoy the show !
