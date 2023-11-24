# Bloggy

Introducing Bloggy! The Open-Source Blogging Platform for developers. It is Built on Python and Django framework and
powers [stacktips.com](https://stacktips.com) blog.

If you are a new contributor to this project, have a look out for issues that have
the [Hacktoberfest](https://github.com/StackTipsLab/Bloggy/issues?q=is%3Aissue+is%3Aopen+label%3Ahacktoberfest) label.

## Key Features

Along with tons of features aimed at enhancing the development and blogging experience.

* **Signup and Login**: Seamlessly create your account and log in to access exclusive content.
* **Magic Link Sign-In**: Forget passwords! We've streamlined the login process with magic link sign-in.
* **Create and Publish**: Share your knowledge with the world by creating and publishing articles, courses, and quizzes
  effortlessly.
* **Customized Admin Dashboard**: Manage your content efficiently with a user-friendly admin dashboard designed with you
  in mind.
* **Sitemaps**: Enhance discoverability with built-in sitemaps that improve search engine ranking.
* **Webmaster Notifications**: Get noticed! StackTips automates Google and Bing webmaster notifications to ensure your
  content reaches a wider audience.

![](https://res.cloudinary.com/practicaldev/image/fetch/s--ahvrJ22X--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/djjung54zz5kanrsk9v2.jpeg)

## Get Involved!

Are you a developer looking to enhance your skills, share your knowledge, or simply be curious about the inner workings
of a developer-centric blog platform? Now's your chance!

Want to contribute right away?

Check out the issues section. https://github.com/StackTipsLab/bloggy/issues

## Installation Guide

Checkout the code from our git repository

    git clone git@github.com:StackTipsLab/bloggy.git

Create a virtual env

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install python dependencies

```shell
pip3 install -r requirements.txt
```

Rename the `.env.example` file to `.env` and provide all the configuration details including Database, and Email
Configurations. Bare minimum, you will need these properties to get started.

```properties
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Your database configuration details
DB_NAME=bloggy
DB_USER=root
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Create and apply database migrations

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

Create superuser

```shell
python3 manage.py createsuperuser
```

Collect static files before publishing or development.

```shell    
python3 manage.py collectstatic
```

Start the application

```shell
python3 manage.py runserver
```

## Bloggy Frontend Module

For building frontend code, you will need the following node version.

```shell
node -v
  v12.22.12
  
npm -v      
  6.14.16  
```

Once you have the above node version installed, install node dependencies using the following command.

```shell
npm install
```

Now, you can build

```shell
npm run start
npm run build # to generate a production build
```

## Importing Demo Content

We currently supports importing the categories from CSV file. This can be done using the `runseed` command. All you need
to do is to provide the base path where your `.csv` files are located.

The sample CSV files are located in `bloggy/demo_content` directory.

```shell
python3 manage.py runseed --dir=demo_content
```

