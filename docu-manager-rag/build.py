from pybuilder.core import use_plugin, init,task
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")

name = "docu-manager-rag"
version = "1.0.0"
default_task = ["clean", "analyze", "publish"]


@init
def set_properties(project):
    project.build_depends_on("fastapi")
    project.build_depends_on("uvicorn")
    project.build_depends_on("httpx")
    project.build_depends_on("langchain")
    project.build_depends_on("openai")
    project.build_depends_on("sqlalchemy")
    project.build_depends_on("psycopg2-binary")
    project.build_depends_on("python-dotenv")
    project.build_depends_on("pytest")
    project.build_depends_on("ollama")
    project.build_depends_on("langchain_community")
    project.build_depends_on("qdrant-client")
    project.build_depends_on("PyPDF2")
    project.build_depends_on("python-docx")
    project.build_depends_on("docx2txt")
    project.build_depends_on("python-multipart")
    project.set_property("coverage_break_build", False)

# @task
# def start():
#     """Start FastAPI app using uvicorn """
#     # command = "set PYTHONPATH=src/main/python && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
#     command = (
#         f"call .\\target\\venv\\Scripts\\activate && "
#         f"set PYTHONPATH=src/main/python && "
#         f"uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
#     )
#     os.system(command)

@task
def start(project, logger):
    """Start FastAPI app using uvicorn"""
    import subprocess
    import sys

    python_executable = sys.executable
    command = [
        python_executable,
        "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = "src/main/python"

    logger.info("Starting FastAPI server...")
    subprocess.Popen(command, env=env)


@task
def create_tables(project, logger):
    """Create database tables programmatically"""
    import sys
    import os
    from sqlalchemy import create_engine
    from dotenv import load_dotenv

    # Set the correct Python path to src/main/python
    src_dir = os.path.join(project.basedir, "src", "main", "python")
    sys.path.insert(0, src_dir)

    # Load environment variables
    load_dotenv()

    try:
        # Import Base from the correct location
        from app.models.models import Base  # Updated import path

        # Create tables
        engine = create_engine(os.getenv("DATABASE_URL"))
        Base.metadata.create_all(bind=engine)
        logger.info(" Database tables created successfully!")
    except ImportError as e:
        logger.error(f"Import failed: {str(e)}")
        logger.error("Current Python path:")
        for path in sys.path:
            logger.error(f" - {path}")
        raise
    except Exception as e:
        logger.error(f"Failed to create tables: {str(e)}")
        raise
