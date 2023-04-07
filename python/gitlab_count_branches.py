import os
from typing import List
from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectBranch

GL_CLIENT = Gitlab(
    url=os.environ.get('GITLAB_HOST', ''),
    private_token=os.environ.get('GITLAB_PRIVATE_TOKEN', None),
    job_token=os.environ.get('GITLAB_JOB_TOKEN', None)
)

if __name__ == '__main__':
    print('Project,Number of Branches')
    projects: Project = GL_CLIENT.projects.list(all=True)
    for project in projects:
        branches: List[ProjectBranch] = project.branches.list(all=True)
        num_of_branch = len(branches)
        print(f'{project.http_url_to_repo},{num_of_branch}')