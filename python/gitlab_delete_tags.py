import os
from typing import List
from gitlab import Gitlab
from gitlab.exceptions import GitlabDeleteError
from gitlab.v4.objects import Project

PROJECT_IDS = [
    # 19,  # Workloads
    13,  # Streaming Kafka
]

DELETE_PROTECTED = False

GL_CLIENT = Gitlab(
    url=os.environ.get('GITLAB_HOST', ''),
    private_token=os.environ.get('GITLAB_PRIVATE_TOKEN', None),
    job_token=os.environ.get('GITLAB_JOB_TOKEN', None)
)

DELETE_TAGS = [
    # "v1.51.0",
]

if __name__ == '__main__':
    # # DELETE non protected
    # for pid in PROJECT_IDS:
    #     project: Project = GL_CLIENT.projects.get(pid)
    #     print('PROJECT: ' + project.name)
    #     branches: List[ProjectBranch] = project.branches.list(all=True)
    #     for branch in branches:
    #         if branch.default:
    #             continue
    #         if not branch.protected or  (branch.protected and DELETE_PROTECTED):
    #             branch.delete()

    # DELETE RELEASE BRANCHES
    for pid in PROJECT_IDS:
        project: Project = GL_CLIENT.projects.get(pid)
        print('PROJECT: ' + project.name)
        for delete_item in DELETE_TAGS:
            try:
                project.tags.delete(delete_item)
                print(f'\t{delete_item}: DELETED')
            except GitlabDeleteError:
                ...
