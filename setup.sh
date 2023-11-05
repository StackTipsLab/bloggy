#!/bin/bash

echo "Creating a virtual environment"
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies from requirements.txt"
pip3 install -r requirements.txt

echo "Configuring Bloggy"

echo "Generating secret key"
SECRET_KEY=$(openssl rand -base64 50)

# Prompt the user for input
echo "Enter SITE_TITLE:"
read SITE_TITLE

# Prompt the user for the database host
read -p "Enter DB_HOST: " DB_HOST
echo -p "Enter DB_PORT: " DB_PORT
echo -p "Enter DB_NAME: " DB_NAME
echo -p "Enter DB_USER: " DB_USER
echo -p "Enter DB_PASSWORD: " DB_PASSWORD

# Create the .env file
cat <<EOF > .env.test
SECRET_KEY=$SECRET_KEY
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DEVELOPMENT_MODE=True

# Your Website details
SITE_TITLE=$SITE_TITLE

# Your Database configurations
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_NAME=$DB_NAME
EOF
echo "Generated .env file with your configurations"

python3 manage.py makemigrations
python3 manage.py migrate

PROJECT_ROOT=$(dirname "${BASH_SOURCE[0]}")
echo ${PROJECT_ROOT}
python3 manage.py runseed --dir=${PROJECT_ROOT}/demo_content