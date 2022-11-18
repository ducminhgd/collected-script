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
        p_branch = _project.protectedbranches.create({
            'name': 'releases/*',
            'merge_access_level': const.AccessLevel.MAINTAINER,
            'push_access_level': const.AccessLevel.NO_ACCESS,
        })
        print(f'{_project.name}\t: Done')
