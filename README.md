# Newsfeed-Application

1.Set up the Python development environment.<br>
2.Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or instead of `python` to start Python):<br>
```    
    pip3 install -r requirements.txt<br> #(superuser = username : admin, password : admin)
    use the below codes if creating a new db file
    python3 manage.py makemigrations<br>
    python3 manage.py migrate<br>
    python3 manage.py createsuperuser # Create a superuser <br>
    python3 manage.py runserver<br>
    
    For schelduler to work run celery and celery beat
    
    celery -A [project-name] worker --loglevel=info
    celery -A [project-name] beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
3. To view news from a country or source use `http://127.0.0.1:8000/api/news` with country or source paremeter
4. If new db file is created use `http://127.0.0.1:8000/api/sources` to populate db file with sources from NewsApi
5. To register a new user use `http://127.0.0.1:8000/api/register`
6. Use `http://127.0.0.1:8000/api/account/` or use Django admin panel to create an Account for the user with setting paremeters.
7. Use `http://127.0.0.1:8000/api/login`to log the user in and use the token for newsfeed calls and use `http://127.0.0.1:8000/api/logout` for logout
8. Use `http://127.0.0.1:8000/api/change-password/`to change user password and use `http://127.0.0.1:8000/api/password_reset/` for reseting the password
9. Use `http://127.0.0.1:8000/api/newsfeed` to view users personalized newsfeed (scheduler is created for new user)
10. Create dot env file with and set SENDGRID_API_KEY = "client secret" for email notifitication to work

## Description 
If a new db file in created then hitting the sources api will populated the db with all the sources from newsapi so the user can select them to set their newsfeed preferences. After account settings preferences are set using the account api or admin panel, the user can use the newsfeed api to see their personalized newsfeed. When the newsfeed api is used for a new user, a django celery task scheduler is created which automatically fetches the news from the newsapi and filters them according to user preferences and updates the newsfeed in the database every 15 minutes. The newsfeed is filters based on the matching sources and country preferences set by the user.If any tagged keyword is appears in any of the filtered news, then an email is sent to the user using the sendgrip api.  
