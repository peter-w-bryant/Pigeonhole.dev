interface Project {
    gh_rep_url: string
    gh_repo_name: string
    pUID: string
    gh_username: string
    gh_contributing_url: string
    num_watchers: string
    num_forks: string
    num_stars: string
    gh_description: string
    date_last_commit: string
    date_last_merged_PR: string
    new_contrib_score: string
}

type ProjectState = {
    projects: Project[]
}

type ProjectAction = {
    type: string
    project: Project
}

type DispatchType = (args: ProjectAction) => ProjectAction