# 🎬 Taller Django Movies App — Workshop 3 IA

Proyecto Django que integra **OpenAI** para enriquecer descripciones de películas, generar imágenes con DALL·E y construir un sistema de recomendación basado en embeddings.

---

## 🖥️ Cómo correr el proyecto en Visual Studio Code

### Paso 1 — Clonar y abrir en VS Code

```bash
git clone <URL_DEL_REPOSITORIO>
cd taller2django
code .
```

Cuando VS Code lo sugiera, instala las **extensiones recomendadas** (aparece una notificación en la esquina inferior derecha).

---

### Paso 2 — Crear el entorno virtual

Abre la **Terminal integrada** de VS Code (`Ctrl+ñ` o `View → Terminal`) y ejecuta:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

> ✅ Verás `(venv)` al inicio de la línea de la terminal cuando el entorno esté activo.

---

### Paso 3 — Seleccionar el intérprete de Python en VS Code

1. Presiona `Ctrl+Shift+P`
2. Escribe **"Python: Select Interpreter"**
3. Elige la opción que muestre `venv` (ejemplo: `./venv/Scripts/python.exe`)

---

### Paso 4 — Instalar dependencias

Con el entorno virtual activo en la terminal:

```bash
pip install -r requirements.txt
```

---

### Paso 5 — Configurar la API Key de OpenAI

Crea el archivo `openAI.env` en la raíz del proyecto (este archivo **no se sube a GitHub**):

```
openai_apikey=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ Reemplaza `sk-xxx...` con la clave entregada por el docente.

---

### Paso 6 — Preparar la base de datos

Ejecuta estos comandos en la terminal de VS Code:

```bash
python manage.py migrate
python manage.py add_movies_db
python manage.py update_movies_from_csv
```

---

### Paso 7 — ▶️ Iniciar el servidor desde VS Code

**Opción A — Con el botón de Play (recomendado):**

1. Ve al panel **Run and Debug** (`Ctrl+Shift+D`)
2. En el menú desplegable de la parte superior selecciona **🚀 Django: Iniciar Servidor**
3. Haz clic en el botón verde ▶️ **Start Debugging** (o presiona `F5`)
4. Abre tu navegador en **http://127.0.0.1:8000**

**Opción B — Desde la terminal:**

```bash
python manage.py runserver
```

---

### Paso 8 — Explorar la aplicación

| URL | Descripción |
|-----|-------------|
| http://127.0.0.1:8000/ | Lista de películas |
| http://127.0.0.1:8000/news/ | Noticias |
| http://127.0.0.1:8000/statistics/ | Estadísticas |
| http://127.0.0.1:8000/recommendations/ | Sistema de recomendación por IA |
| http://127.0.0.1:8000/admin/ | Panel de administración Django |

---

## 🤖 Comandos del Workshop 3 (con VS Code Run & Debug)

Todos estos comandos están configurados en `.vscode/launch.json` y se pueden ejecutar directamente desde el panel **Run and Debug**:

| Configuración VS Code | Comando Django | Descripción |
|-----------------------|----------------|-------------|
| 🎬 Cargar Películas | `add_movies_db` | Carga 50 películas en la BD |
| 📝 Actualizar Descripciones desde CSV | `update_movies_from_csv` | Actualiza todas las descripciones con el CSV incluido |
| 🤖 Actualizar Descripción con OpenAI | `update_descriptions` | Actualiza la descripción de la **primera** película usando GPT |
| 🖼️ Generar Imagen con OpenAI | `update_images` | Genera imagen DALL·E de la **primera** película |
| 📁 Cargar Imágenes desde Carpeta | `update_images_from_folder` | Asigna imágenes de `media/movie/images/` a las películas |
| 🔢 Generar Embeddings | `movie_embeddings` | Genera y almacena embeddings para todas las películas |
| 📐 Comparar Similitud | `movie_similarities` | Compara dos películas y un prompt con similitud de coseno |

> ⚠️ Los comandos que llaman a OpenAI requieren el archivo `openAI.env` configurado.

---

## 📁 Estructura del Proyecto

```
taller2django/
├── .vscode/                        # Configuración de VS Code
│   ├── launch.json                 # Configuraciones de ejecución/depuración
│   ├── settings.json               # Ajustes del editor
│   └── extensions.json             # Extensiones recomendadas
├── movie/                          # App principal de películas
│   ├── management/commands/        # Comandos personalizados de Django
│   │   ├── add_movies_db.py
│   │   ├── update_descriptions.py
│   │   ├── update_movies_from_csv.py
│   │   ├── update_images.py
│   │   ├── update_images_from_folder.py
│   │   ├── movie_embeddings.py
│   │   └── movie_similarities.py
│   └── models.py                   # Modelo Movie (title, genre, year, description, image, emb)
├── recommendations/                # App de recomendaciones por IA
├── news/                           # App de noticias
├── moviereviews/                   # Configuración principal Django
├── updated_movie_descriptions.csv  # Descripciones generadas por IA para 50 películas
├── movies.json                     # Datos base de 50 películas en español
├── requirements.txt                # Dependencias del proyecto
└── openAI.env                      # ⚠️ API Key (NO subir a GitHub — en .gitignore)
```

---

## 🔒 Seguridad

- El archivo `openAI.env` está en `.gitignore` y **nunca debe subirse a GitHub**.
- Verifica siempre con `git status` que `openAI.env` no aparezca en los archivos a confirmar antes de hacer `git add`.

