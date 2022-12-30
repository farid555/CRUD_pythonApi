# CRUD_pythonApi

create virtual Env: py -3 -m venv [anyName] 
command Palette :venv\Scripts\python.exe
In terminal command: venv\scripts\activate
install: pip install "fastapi[all]"
it will show what we install the driver: pip freeze
run the main: uvicorn main:app --reload
http://127.0.0.1:8000/docs
create app folder and file __init__.py
moved to main.py inside app folder
run command uvicorn app.main:app --reload

pip install psycopg2 ....install for MySQL