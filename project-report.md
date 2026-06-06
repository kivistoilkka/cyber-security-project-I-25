# Project report


LINK: https://github.com/kivistoilkka/cyber-security-project-I-25
README.md contains installation instructions.

FLAW 1:
https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py#L26
https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py#L52

This flaw demonstrates Broken Access Control (CWE-862: Missing Authorization). There has to be some notes saved to the database. Any user can view any note by simply going to the url of the note (e.g. http://localhost:8000/note/1/). Also, using https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/attacks/flaw1_bac.html attacker can delete notes with id numbers between 1 and 100 from the database. 

This flaw can be fixed by enforcing user login with @login_required decorators and checking if user is the owner of the note before showing, deleting or updating it. These fixes can be applied in https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py by uncommenting all the lines containing "# Flaw1" and commenting line 52.

FLAW 2:
https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py#L71-L73

This flaw demonstrates Injection (CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')). There has to be some notes saved to the database for two different users. One of the users, the attacker, opens one of their notes and updates it with the following text:

ALL YOUR BASE ARE BELONG TO US" WHERE id = [X] OR '1'='1' --

, where [X] is the id number of the note visible in the address bar (see https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/screenshots/flaw-2-before-3.png). Now all of the notes for all of the users have been changed to "ALL YOUR BASE ARE BELONG TO US". To blank all of the notes, the attacker can use the following text:

"; --

This flaw is fixed by simply using Django's model objects to interact with the database, since those are designed to keep SQL code and parameters of the query separate and the database driver escapes user-provided parameters. These fixes can be applied in https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py by uncommenting lines containing "# Flaw2" and commenting lines 71-73.

FLAW 3:
https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/config/settings.py#L32

This flaw demonstrates Security Misconfiguration (CWE-756: Missing Custom Error Page). Let's assume this application is in production and it is run with command "python3 src/manage.py runserver". When user is logged in and goes to http://localhost:8000/update/1/ with a browser, Django automatically shows a lot of debug data, including environmental variables and Python version. This is information which attacker can potentially use to find a way to break into the system.

This flaw can be fixed by making sure the app is deployed correctly when taken to the production. Using command "python3 src/manage.py check --deploy" we get a list of warnings. By fixing most of them in file https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/config/settings.py by uncommenting all the lines containing "# Flaw3" (skipping SSL configurations in this demonstration), commenting lines 28, 32 and 35 and adding .env -file to /src, we are ready to correctly deploy the application using gunicorn. The .env -file can be created using the following command (with a new secret key, one in the command is an example):

echo "SECRET_KEY = \"ihgrep974tPgsTrfa=Yhiheg8W4HRGryaehrIu6sH2EIPHihip39Y08THIreyaEyaeWyyaHG8Hhyaerhy\"" > src/.env

If we now run command "python3 src/manage.py check --deploy", we see that there are only two issues remaining (the ones related to SSL configurations). Deployed application can be run with command "cd src && gunicorn config.wsgi". The application is now running using production server and when we now go to http://localhost:8000/update/1/, we see more generic "Server Error (500)" message, which reveals very little of the server infrastructure.

FLAW 4:
This flaw demonstrates Identification and Authentication Failure (CWE-307: Improper Restriction of Excessive Authentication Attempts). If this demonstration is done after fixing flaw 3, disable CSRF token check by recommenting lines 85-86 in https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/config/settings.py or restore the whole file to it's previous state. Create user with name "Tester" and with password "12computer34". By running command "python3 attacks/flaw4_iaf.py http://localhost:8000/login/ Tester attacks/flaw4_candidates.txt", different passwords are tried to log in as the user Tester using brute force and we can see that this user is using password listed in file attacks/flaw4_candidates.txt.

To mitigate this problem, we can use Axes plugin in our website to block login attempts from one source after too many failures. To enable it, uncomment lines containing "# Flaw4" in https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/config/settings.py, then create necessary tables to the database with command "python3 src/manage.py migrate". Note that lines 148 and 149 are set so that locks are based on the username, not the IP address of the attacker. This is mainly to make this demonstration a little bit easier to run, but there are also data privacy concerns regarding storage of IP addresses (see https://django-axes.readthedocs.io/en/latest/3_usage.html#data-privacy-and-gdpr).

If we now try to run our attack script, we get None result. If we try to login as Tester, we see message "Account locked: too many login attempts. Please try again later." and all login attempts for the user are blocked for 15 minutes. We can allow access for user Tester from Django admin UI by going to Axes -> Access attempts and removing all login attempts by the user, or we can reset all lockouts with command "python3 src/manage.py axes_reset".

FLAW 5:
https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/requirements.txt#L5

This flaw demonstrates Vulnerable and Outdated Components. There has to be some notes saved to the database for multiple users. The application uses Django version 5.2.7, which has vulnerability CVE-2025-64459 ("Potential SQL injection via _connector keyword argument in QuerySet and Q objects", https://www.djangoproject.com/weblog/2025/nov/05/security-releases/ and https://github.com/0xCyberstan/CVE-2025-64459-Poc). After logging in, the user can search notes, which will be shown in a separate search page . By adding "&_connector=)OR%201=1%20OR(" to the end of the search url [e.g. http://localhost:8000/search/?note_text=Find+this&_connector=)OR%201=1%20OR( ], user is able to list all of the notes in the database, not just their own.

This flaw is fixed in Django version 5.2.8, so we can update the Django version with command "pip install django==5.2.8 && pip freeze > requirements.txt" (latest update would be preferable, but those are not tested for anything breaking this demonstration). If we now try to add malicious payload to our url, we get "TypeError: The following kwargs are invalid: '_connector'". We can also fix our code to sanitize user provided filters as described in the POC by uncommenting lines containing "# Flaw5" in https://github.com/kivistoilkka/cyber-security-project-I-25/blob/main/src/pages/views.py. This is generally highly recommended practice as there may be other ways to inject SQL using user provided filters and in this case we also avoid causing the TypeError which we should handle anyway.