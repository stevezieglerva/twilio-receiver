rm /Users/sziegler/Documents/GitHub/twilio-receiver/data/s3/test/reminders_db.json
rm /Users/sziegler/Documents/GitHub/twilio-receiver/data/s3/prod/reminders_db.json

aws s3 sync s3://twilio-apps/ s3/