from MTQCApp.commprotocol.server_response import SUCCESS, WRONG_JSON
from MTQCApp.models import Project


def new_project(project_data, user):
    try:
        project_name = project_data["project_name"]
    except KeyError:
        return {"status": WRONG_JSON}
    project = Project(name=project_name, path="./", user=user)
    project.save()
    return {"status": SUCCESS, "project": project}
