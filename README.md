# Taller Django Movies App

## Instalación

1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  (Mac/Linux)
venv\Scripts\activate     (Windows)

2. Instalar dependencias
pip install -r requirements.txt

3. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

4. Cargar películas
python manage.py add_movies_db

5. Ejecutar servidor
python manage.py runserver
