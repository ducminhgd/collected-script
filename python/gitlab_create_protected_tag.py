import os
from typing import List
from gitlab import Gitlab, const
from gitlab.v4.objects import Project

GL_CLIENT = Gitlab(
    url=os.environ.get('GITLAB_HOST', ''),
    private_token=os.environ.get('GITLAB_PRIVATE_TOKEN', None),
    job_token=os.environ.get('GITLAB_JOB_TOKEN', None)
)

if __name__ == '__main__':
    projects: List[Project] = GL_CLIENT.projects.list(all=True)
    for _project in projects:
        try:
            _project.protectedtags.create({'name': '*', 'create_access_level': const.MAINTAINER_ACCESS})
            print(f'{_project.name}\t: Done')
        except:
            print(f'{_project.name}\t: Error')
