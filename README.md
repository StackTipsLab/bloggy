# Bloggy - Django Powered Blog

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

Rename the `.env.example` file to `.env` and provide all te configurations details including Database, Email Configurations. 

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
npm run build # to generate production build
```
