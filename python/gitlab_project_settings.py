import os
from typing import List
from gitlab import Gitlab
from gitlab.v4.objects import Project

SKIP_PROJECT_IDS = [
    19,  # Workloads
    28,  # Cloud DNS
]

GL_CLIENT = Gitlab(
    url=os.environ.get('GITLAB_HOST', ''),
    private_token=os.environ.get('GITLAB_PRIVATE_TOKEN', None),
    job_token=os.environ.get('GITLAB_JOB_TOKEN', None)
)

if __name__ == '__main__':
    projects: List[Project] = GL_CLIENT.projects.list(all=True)
    for _project in projects:
        if _project.get_id() in SKIP_PROJECT_IDS:
            print(f'{_project.name}\t:\tSkipped')
            continue
        _project.merge_method = 'ff'
        _project.squash_option = 'default_on'
        _project.save()
        print(f'{_project.name}\t:\tDone')
