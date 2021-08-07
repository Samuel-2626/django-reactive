# Full-Stack Reactive Website in Django (no JavaScript)

Modern website that require complex user interaction are built using a dedicated fronted framework like React, Vue among others. However, their are some complexity that goes with it. Based on experience, trying this route of building a full-stack application we have time complexity, more money to host the dedicated frontend, SEO complexity, syntax differences, in some cases duplicate business logic and a whole lot more.

We can achieve the same reactive website with technologies like React without leaving our Django project or addding another language to our toolkit. It therefore is less complex, less code and has a faster development time.

There are several technologies out there that achieves these functionality for us like [Sockpuppet](https://sockpuppet.argpar.se/), [reactor](https://github.com/edelvalle/reactor/) and [Unicorn](https://www.django-unicorn.com/docs/). However, for this tutorial we would be taking a look at Unicorn to achieve interactivity within our website without any custom JavaSript.

Before we proceed, note that there may be benefits of using a dedicated frontend for instance useful to have a dedidcated team responsible for the frontend and backend.

## Project Setup and Overview

Here's a quick look at the app you'll be building:

![Home Page](https://github.com/Samuel-2626/django-reactive/blob/main/images/homepage-2.png)

We can add a new book, and delete a new book without refreshing the page, same functionality that would be possible with SPAs.

Clone down the [base](https://github.com/Samuel-2626/django-reactive/tree/base) branch from the [django-reactive](https://github.com/Samuel-2626/django-reactive) repo:

```bash
$ git clone https://github.com/Samuel-2626/django-reactive --branch base --single-branch
$ cd django-reactive
```

We'll use Docker to simplify setting up and running Django with the dependencies.

From the project root, create the images and spin up the Docker containers:

```bash
$ docker-compose up -d --build
```

Next, apply the migrations and create a superuser:

```bash
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py createsuperuser
```

Once done, navigate to [http://127.0.0.1:8080/](http://127.0.0.1:8080/) to ensure the app works as expected. You should see the following:

![Home Page](https://github.com/Samuel-2626/django-reactive/blob/main/images/homepage.png)

Take note of the `Book` model in _books/models.py_:

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
```

## Unicorn

[Unicorn](https://www.django-unicorn.com/docs/) is a reactive component framework that progressively enhances a normal Django view, makes AJAX calls in the background, and dynamically updates the DOM. It seamlessly extends Django past its server-side framework roots without giving up all of its niceties or re-building your website.

Let's add it to our installed application

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    "django_unicorn",
    # Local
    'books.apps.BooksConfig',
]
```

Next, update your project `urls.py` file like so:

```py
path("unicorn/", include("django_unicorn.urls")), # new
```

## Project URLs, Views & Template

In this section, we will be setting up our project URLs, Views and Templates using Django without Unicorn.

Next, update your project `urls.py` file like so:

```py
path("", views.index), # new
```

Next, update your books application `views.py` like so:

```py
def index(request):
    return render(request, "index.html", {})
```

Next, update your books template `index.html` like so:

```html
{% load unicorn %}

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<title>Django Books</title>

		<link
			href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
			rel="stylesheet"
			integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
			crossorigin="anonymous"
		/>
		{% unicorn_scripts %}
	</head>
	<body>
		{% csrf_token %}
		<div class="container">
			<h2>Favourite Django Books</h2>

			{% unicorn 'book' %}
		</div>
	</body>
</html>
```

## Conclusion
