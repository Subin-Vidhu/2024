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

    