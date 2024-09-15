from pathlib import Path
from os import listdir
from os.path import isfile, join, dirname
from http import HTTPStatus

from fastapi import HTTPException
from importlib import import_module
from yaml import safe_load


def get_name_project_file(project_name, stage_name):
    path = PATH_TO_PROJECTS
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        with open(f"{PATH_TO_PROJECTS}{file}", "r") as service:
            data = safe_load(service)
            if data["name"] == project_name:
                if data["stages"]["stage_name"] == stage_name:
                    return file
                else:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_REQUEST,
                        detail=(
                            f"Not found stage '{stage_name}' "
                            f"in project '{project_name}'."
                        )
                    )
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=f"Not found project '{project_name}' "
    )


def get_path_to_projects():
    parent_dir_path = dirname(dirname(__file__))
    if "pytest_tests" in parent_dir_path:
        return Path(__file__).parents[1]
    return parent_dir_path


PATH_TO_PROJECTS = get_path_to_projects() + "/projects/"
Path_TO_CONFIG = get_path_to_projects() + "/base_configs/"


def get_patch_schema(project_name):
    with open(f"{PATH_TO_PROJECTS}{project_name}", "r") as service:
        data = safe_load(service)["proto_name"].split(".")
        data[0] = data[0] + "_pb2"
        protobuf = import_module(f"proto.{data[0]}")
        return getattr(protobuf, data[1])


def get_initial_config(project_name):
    with open(f"{PATH_TO_PROJECTS}{project_name}", "r") as service:
        data = safe_load(service)["default_config"]
        with open(f"{Path_TO_CONFIG}{data}", "r") as config_name:
            return safe_load(config_name)
