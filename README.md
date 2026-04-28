# Securización del chatbot basado en RAG para consultas de Embarazadas.

Este proyecto usa como base el chatbot creado en la **[Práctica 4](https://github.com/JorgeCM2004/AIA_Practica4)** y extiende su funcionamiento con el uso de técnicas de anonimización de información sensible, securización contra "prompt injection" y encriptación de la base de datos vectorial creada en la **[Práctica 2](https://github.com/JorgeCM2004/AIA_Practica2)**.

Destaca por su diseño modular orientado a objetos y el uso de **[uv](https://github.com/astral-sh/uv)** para una gestión del entorno y dependencias ultrarrápida y reproducible.

## Estructura del Proyecto

El código está organizado en distintos módulos para facilitar su lectura y mantenimiento:
```
├── 📁 test
│   ├── 🐍 anonymization_test.py
│   └── 🐍 security_test.py
├── 📁 utils
│   ├── 📁 agent
│   │   ├── 🐍 F_Decision_Graph_Agent.py
│   │   ├── 🐍 F_Linear_Graph_Agent.py
│   │   ├── 🐍 F_Tools_Graph_Agent.py
│   │   └── 🐍 __init__.py
│   ├── 📁 builder
│   │   └── 🐍 F_Knowledge_Builder.py
│   ├── 📁 downloader
│   │   └── 🐍 F_Data_Downloader.py
│   ├── 📁 searcher
│   │   ├── 🐍 F_Hybrid_Searcher.py
│   │   ├── 🐍 F_Lexical_Searcher.py
│   │   └── 🐍 F_Semantic_Searcher.py
│   ├── 📁 security
│   │   ├── 🐍 F_Encrypter.py
│   │   ├── 🐍 F_anonymizer.py
│   │   ├── 🐍 F_prompt_injection.py
│   │   └── 🐍 __init__.py
│   └── 🐍 __init__.py
├── ⚙️ .gitignore
├── 📝 README.md
├── 📄 env_template
├── 🐍 main.py
├── ⚙️ pyproject.toml
└── 📄 uv.lock
```

> ⚠️ **IMPORTANTE: Credenciales de Kaggle**
>
> Este proyecto utiliza la API de Kaggle para descargar el dataset automáticamente. Para que funcione, necesitas tener configurado tu archivo de credenciales (`kaggle.json`).
>
> **Pasos para configurarlo:**
> 1. Inicia sesión en [Kaggle](https://www.kaggle.com/) y ve a los ajustes de tu cuenta (*Settings*).
> 2. Haz clic en **"Create New Token"** para descargar el archivo `kaggle.json`.
> 3. Guarda este archivo en la siguiente ruta dependiendo de tu sistema operativo:
>    - **Windows:** `C:\Users\<TuUsuario>\.kaggle\kaggle.json`
>    - **macOS / Linux:** `~/.kaggle/kaggle.json`

## 1. Instalación de `uv`

Si aún no tienes el gestor de paquetes `uv` instalado en tu sistema, abre tu terminal y ejecuta el comando correspondiente a tu sistema operativo:

**Para macOS y Linux:**
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

**Para Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

## 2. Instalación de Ollama

Este proyecto utiliza modelos de lenguaje ejecutados en local para garantizar la privacidad de los datos. Para ello, necesitamos instalar la herramienta **Ollama** y descargar el modelo de Meta.
* **Windows y macOS:** Dirígete a la [página oficial de descarga de Ollama](https://ollama.com/download) y baja el instalador correspondiente para tu sistema.
* **Linux:** Puedes instalarlo directamente ejecutando en tu terminal:
  ```bash
  curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
  ```

## 3. Instalación de Llama3.2

Una vez instalado Ollama, asegúrate de que la aplicación está abierta. Luego, abre una nueva terminal y ejecuta el siguiente comando para descargar el cerebro de nuestro agente:
```bash
ollama run llama3.2
```
*(Nota: La primera vez que ejecutes este comando, tardará unos minutos en descargar el modelo. Una vez que termine la descarga y te aparezca un prompt de chat en la consola, puedes salir escribiendo `/bye` o cerrando la terminal).*

## 4. Configuración del Entorno

Como este proyecto utiliza `pyproject.toml` y `uv.lock`, la configuración es automática. Abre la terminal en la carpeta raíz del proyecto y ejecuta:

```bash
uv sync
```
*Este comando creará automáticamente el entorno virtual (`.venv`) e instalará las versiones exactas de las librerías (langchain, chromadb, etc.) definidas en el archivo lock, garantizando que todo funcione a la primera.*

## 5. Ejecución del Código

Para ejecutar el programa principal, descargar el dataset automáticamente y empezar a hablar con el chatbot mediante terminal, simplemente lanza:

```bash
uv run main.py
```

## 6. Ejecución de los Tests

Para ejecutar de manera automática los tests que se realizaron para comprobar el funcionamiento de las técnicas de securización, simplemente lanza:

```bash
uv run python -m pytest .\test\
```
