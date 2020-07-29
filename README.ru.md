# Questions & Answers

| [English version](https://github.com/KonstErz/s_web_project/blob/master/README.md) |

### The service is implemented using the Django web framework tools.

---


## Purpose

The project is a service of answering questions. The user of the service has the opportunity to register, ask a question, answer questions from other users. Also, the user can mark the questions using the "Like" button, changing their rating.

## Main project entities

1. User: username, password, email;
2. Question: title, text, author, publish date, rating;
3. Answer: text, question, publish date, author;
4. Like: question, user.

## Forms and project pages

(see examples of screenshots of pages in the project directory */public/img/*)

+ **Main page**

URL: /

Purpose: is a list of new questions, sorted by the date they were added, starting with the most recent. The list is displayed using pagination, 10 questions are displayed on one page.

+ **List of popular questions**

URL: /popular/

Purpose: is a list of "popular" questions. The list displays questions in descending order of rating using pagination. 10 questions are displayed on one page.

+ **Single question page**

URL: /question/12/ (where 12 - question_id)

Purpose: on this page you can see the text of the question, the author, the date and time of publication, the rating and the list of answers to the question. This page can only be viewed by authorized users. Authorized users can "Like" the question and can add their own answer.

+ **Registration page**

URL: /signup/

Purpose: the user can enter his name, email, password and register in the project.

+ **Login page**

URL: /login/

Purpose: the user can enter his name and password and authorize (log in) in the project.

+ **Add question page**

URL: /ask/

Purpose: an authorized user can ask a question and then go to the page of this question.

+ **Like/Dislike system**

URL: /like/

Purpose: the user can click the "Like" button for the question and this will increase the rating of the question. The user can put "Like" no more than 1 time for 1 question. If the user no longer likes the question, then he can click the "Dislike" button and this will return the question's rating back. The Like/Dislike system is implemented using AJAX requests.

---


### Quick start guide for starting a service on your local computer

1. Create a folder for the project called 'project_name'. Go to this folder and clone the repository with the project:

    ```
    git clone https://github.com/KonstErz/s_web_project.git
    ```

2. Create a virtual python3 environment in the same folder using *virtualenv*:

    ```
    virtualenv -p python3 venv
    ```

where *'venv'* is the name of the virtual environment. If you don't have virtualenv installed, you can install it using the commands:

    ```
    sudo apt update
    sudo apt install virtualenv
    ```

and also must have Python3 installed on your system (python 3.6+ recommended).

3. Activate the virtual environment:

    ```
    . venv/bin/activate
    ```

4. Go to the project folder and call the command to set all requirements:

    ```
    bash commands_2.sh
    ```

Can check if Python finds Django module:

    ```
    python3 -m django --version
    ```

5. This project can work on 2 databases: MySQL (by default) and SQLite 3. You need to go to the MySQL console client (from the root password) and create a database for the Django web application to work:

    ```
    mysql -u root -p
    
    mysql> CREATE DATABASE askapp CHARACTER SET utf8;
    mysql> CREATE USER 'django'@'localhost' IDENTIFIED BY 'passwrd123';
    mysql> GRANT ALL PRIVILEGES ON askapp.* TO 'django'@'localhost';
    mysql> FLUSH PRIVILEGES;
    ```

To exit MySQL use the key combination Ctrl+D.

6. Go to the *'ask'* directory of the project with *manage.py* file, apply all migrations, create a superuser and start the server:

    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser
    python3 manage.py runserver
    ```

Now you can go to the server http://localhost:8000/ in your browser. Try to register a test user in the system, add new questions and answers. Ctrl+C - to exit debug mode of a web application and `deactivate` - command to exit the virtual environment.

### Quick guide to starting the service in the testing terminal of the online course "Web Technologies"

**Attention! You may have difficulty making decisions at certain points in the course. This is due to outdated versions of modules and instability of validation tests. Further reading the comments for the lesson may help you solve your problem.**

1. After starting the testing VM, clone the repository with the project to the */home/box/web* directory:

    ```
    git clone https://github.com/KonstErz/s_web_project.git /home/box/web
    ```

2. Go to the */home/box/web* directory and run the command to install the requirements:

    ```
    sudo bash commands_1.sh
    ```

3. On a test system, the nginx http server should listen on port 80 by default and proxy client requests to the gunicorn application server host, which uses django as a wsgi application to handle requests. Commands for connecting servers are in the *init.sh* file:

    ```
    bash init.sh
    ```

4. You may experience unexpected exceptions from MySQL side, so try running your project with the default SQLite 3 database. To do this, edit the *home/box/web/ask/ask/settings.py* file using the *nano* editor: in the *DATABASES* section, remove the *mysql* section and set the database name *'sqlite3'* to *'default'*. The section should look like this:

    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    ```

5. Go to *home/box/web/ask* directory and do all the necessary migrations:

    ```
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```


