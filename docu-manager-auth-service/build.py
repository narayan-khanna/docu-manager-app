from pybuilder.core import use_plugin, init,task
import os

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin("python.install_dependencies")

name = "docu-manager-auth-service"
version = "1.0.0"
default_task = ["clean", "analyze", "publish"]


@init
def set_properties(project):
    project.build_depends_on("fastapi")
    project.build_depends_on("uvicorn")
    project.build_depends_on("sqlalchemy")
    project.build_depends_on("psycopg2-binary")
    project.build_depends_on("passlib[bcrypt]")
    project.build_depends_on("bcrypt==4.0.1")
    project.build_depends_on("python-dotenv")
    project.build_depends_on("python-jose")
    project.build_depends_on("pydantic")
    project.set_property("coverage_break_build", False)


@task
def start():
    """Start FastAPI app using uvicorn """
    command = "set PYTHONPATH=src/main/python && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
    os.system(command)


@task
def create_tables():
    """Start FastAPI app using uvicorn """
    print("[TASK] Creating tables...")
    command = "set PYTHONPATH=src/main/python  && python run_create_db.py"
    os.system(command)
