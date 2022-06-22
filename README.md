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
3. To view news from a country or source use `http://127.0.0.1:8000/news` with country or source paremeter
4. If new db file is created use `http://127.0.0.1:8000/sources` to populate db file with sources from NewsApi
5. To register a new user use `http://127.0.0.1:8000/register`
6. Use admin panel to create an Account for the user with setting paremeters. (Api cannot be used as DRF does provide list of drop-downs)
7. Use `http://127.0.0.1:8000/login`to log the user in and use the token for newsfeed calls
8. Use `http://127.0.0.1:8000/newsfeed` to view users personalized newsfeed (scheduler is created for new user)
9. Create dot env file with and set SENDGRID_API_KEY = "client secret"
