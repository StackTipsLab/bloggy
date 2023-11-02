python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runseed --dir=/Users/nilanchal.panigrahy/Documents/github/StackTipsLab/bloggy/demo_content