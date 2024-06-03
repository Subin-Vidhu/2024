# Django

### Introduction

![alt text](image.png)

 - Django is an open-source web framework that is written in Python.
 - It is a high-level web framework that encourages rapid development and clean, pragmatic design.

### What is Django?

 - Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.
 - It is a free and open-source web framework that follows the model-template-views architectural pattern.
 - Django is maintained by the Django Software Foundation (DSF), an independent organization established as a 501(c)(3) non-profit.
- Django's primary goal is to ease the creation of complex, database-driven websites.
- Django emphasizes reusability and "pluggability" of components, rapid development, and the principle of DRY (Don't Repeat Yourself).
- Python is used throughout, even for settings files and data models.
- Django also provides an optional administrative create, read, update and delete interface that is generated dynamically through introspection and configured via admin models.
- Some well-known sites that use Django include PBS, Instagram, Mozilla, The Washington Times, Disqus, Bitbucket, and Nextdoor.
- Django applications can be used with any client-side framework, and there are several options available for the front-end.
- Django admin is a built-in app that automatically generates a user interface to add and modify content in the database.
- Django REST framework is a powerful and flexible toolkit for building Web APIs.
- Django applications include some reusable components and more can be added to meet the requirements of a particular application.

### Features of Django

 - **Ridiculously fast** − Django was designed to help developers take applications from concept to completion as quickly as possible.
 - **Reassuringly secure** − Django takes security seriously and helps developers avoid many common security mistakes.
 - **Exceedingly scalable** − Some of the busiest sites on the planet use Django’s ability to quickly and flexibly scale to meet the heaviest traffic demands.
 - **Incredibly versatile** − Companies, organizations, and governments have used Django to build all sorts of things — from content management systems to social networks to scientific computing platforms.
 - **Easy to learn** − Django was designed to be easy to learn and use.
 - **Free and open-source** − Django is free and open source, and it's easy to download and use.

### Course Content

- Syllabus: [Django-web-framework-Meta-Backend-course](https://www.coursera.org/learn/django-web-framework/supplement/LNFwv/course-syllabus)

### Python Installation

- installing-python-optional-for-windows-users: [Python Installation](https://www.coursera.org/learn/django-web-framework/supplement/NFk5o/installing-python-optional-for-windows-users)


### Setting up a project in VS Code

- setting-up-a-project-in-vs-code: [Setting up a project in VS Code](https://www.coursera.org/learn/django-web-framework/supplement/OdgJH/setting-up-a-project-in-vs-code)


### working-with-virtual-environments-on-your-local-machine

- working-with-virtual-environments-on-your-local-machine: [Working with virtual environments on your local machine](https://www.coursera.org/learn/django-web-framework/supplement/rZlSl/working-with-virtual-environments-on-your-local-machine)

### Working with labs in the course

- working-with-labs-in-the-course: [Working with labs in the course](https://www.coursera.org/learn/django-web-framework/supplement/b35Pn/working-with-labs-in-this-course)

### Django Installation

- Django installation steps:

    - Step 1: Install Django
    - Step 2: Verify the installation
    - Step 3: Create a Django project
    - Step 4: Create a Django app
    - Step 5: Start the Django development server

    - eg.
        ```python
        pip install Django
        django-admin --version
        django-admin startproject mysite
        cd mysite
        python manage.py runserver
        ```

- To run and view your Django app in the browser, execute the following command in terminal. (Verify you are in the directory where manage.py file resides.)
    
    ```python
    python3 manage.py runserver # To run the server
    python3 manage.py makemigrations # To compile the migrations
    python3 manage.py migrate  # To migrate the changes in Database
    ```

### Additional Resources

    - [Additional Resources](https://www.coursera.org/learn/django-web-framework/supplement/yqDlw/additional-resources)

### Project and Apps

- Basic structure of a webpage:
    
    - A webpage is made up of HTML, CSS, and JavaScript.
    - HTML is the structure of the webpage.
    - CSS is the styling of the webpage.
    - JavaScript is the interactivity of the webpage.

- Django project structure:

    - A Django project is made up of multiple apps.
    - Each app is a separate module that is designed to do one thing well.
    - Each app can be reused in multiple projects.
    - Each app can be developed by a separate team.

- What is required to create a dynamic web application?

    ![alt text](image-1.png)

    ![alt text](image-3.png)

    - Client sends a request to the server.
    - Database is used to store and retrieve data.
    - Server processes the request and sends a response back to the client, after fetching data from the database.
    - Client receives the response and displays the data.
    - The client can be a web browser, mobile app, or desktop app.
    - The server can be a web server, application server, or database server.
    - The database can be a relational database, NoSQL database, or in-memory database.
    - The client and server communicate using HTTP or HTTPS.
    - The server and database communicate using SQL or NoSQL queries.

- Django project structure: [Refer me](https://www.coursera.org/learn/django-web-framework/supplement/Ahqrc/project-structure)

    - PROJECT
        - In Django, a project represents the entire web application.
        - A project is made up of multiple apps.
        - Django provides a set of commands that automate the creation of projects and apps.
        - A project is a collection of settings, URLs, and apps.
        - Project structure means to organize the files and folders in a project.
        - This allows developers to code rather than configuration.
        - Django follows the DRY principle, which means Don't Repeat Yourself.

            ![alt text](image-5.png)

    - APP
        - In Django, an app represents a specific feature or functionality.
        - An app is a web application that does something.
        - An app is a collection of models, views, templates, and URLs.
        - An app can be reused in multiple projects.
        - An app can be developed by a separate team.
        - An app can be distributed as a package.
        - An app can be installed using pip.

            ![alt text](image-4.png)

    - For Django to recognize an app, it must be added to the INSTALLED_APPS list in the settings.py file.

        - ![alt text](image-6.png)

    - ![alt text](image-7.png)

### Creating a Django project

- Create a new directory for the project.

    ```python
    mkdir myproject
    cd myproject
    ```

- Virtualenv is a tool to create isolated Python environments.
    - Virtualenv is used to manage dependencies for different projects.
    - Virtualenv is used to avoid conflicts between dependencies.

    - To create a virtual environment, execute the following command in terminal.

        - Linux/Mac:
            ```python
            python3 -m venv myenv
            source myenv/bin/activate
            ```

        - Windows:
            ```python
            python -m venv myenv
            myenv\Scripts\activate
            ```


    - To install Django in the virtual environment, execute the following command in terminal.

        ```python
        pip install Django
        ```

    - To check the Django version, execute the following command in terminal.

        - 
            ```python
            django-admin --version
            ```

            OR

        -
            ```python
            python -m django --version
            ```

    - To create a Django project, execute the following command in terminal.

        ```python
        django-admin startproject mysite
        ```

    - To create a Django app, execute the following command in terminal.

        ```python
        python manage.py startapp myapp
        ```

    - To run the Django development server, execute the following command in terminal.

        ```python
        python manage.py runserver
        ```

    - To stop the Django development server, press Ctrl + C in terminal.

    - To deactivate the virtual environment, execute the following command in terminal.

        ```python
        deactivate
        ```

### Admin and Structures

- When working with Django projects, developer has 2 choices for command line utility:
    - django-admin
    - manage.py

        - django-admin is Django's command-line utility for administrative tasks.

        - manage.py is a thin wrapper around django-admin that takes care of several things for you.

        - django-admin vs manage.py:

            - django-admin
                - django-admin is Django's command-line utility for administrative tasks.
                - django-admin is a standalone program that is installed along with Django.
                - django-admin is used to create projects, apps, and other administrative tasks.
                - django-admin is used to manage the Django project as a whole.
                - django-admin is used to run management commands.
                - django-admin is used to start the development server.
            
            - manage.py
                - manage.py is a thin wrapper around django-admin that takes care of several things for you.
                - manage.py is a Python script that is created in the project directory.
                - manage.py is used to run management commands.
                - manage.py is used to start the development server.
                - manage.py is used to create an app.
                - manage.py is used to create a superuser.
                - manage.py is used to run migrations.

            - django-admin.py 

                - automatically installed
                - located on system path
                - activate virtual environment

            - manage.py
                
                - automatically created each time you create a new project
                - located in the project directory
                - specific to the virtual environment
                - points to the settings.py file in the project directory

        ![alt text](image-8.png)
    