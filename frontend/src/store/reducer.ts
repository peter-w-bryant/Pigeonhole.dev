import * as actionTypes from "./actionTypes"

const initialState: ProjectState = {
  projects: [],
}

const reducer = (
    state: ProjectState = initialState,
    action: ProjectAction
  ): ProjectState => {
    switch (action.type) {
      case actionTypes.ADD_PROJECT:
        // eslint-disable-next-line no-case-declarations
        const newProject: Project = {
            gh_rep_url: action.project.gh_rep_url,
            gh_repo_name: action.project.gh_repo_name,
            pUID: action.project.pUID,
            gh_username: action.project.pUID,
            gh_contributing_url: action.project.gh_contributing_url,
            num_watchers: action.project.num_watchers,
            num_forks: action.project.num_forks,
            num_stars: action.project.num_stars,
            gh_description: action.project.gh_description,
            date_last_commit: action.project.date_last_commit,
            date_last_merged_PR: action.project.date_last_merged_PR,
            new_contrib_score: action.project.new_contrib_score,
        }
        return {
          ...state,
          projects: state.projects.concat(newProject),
        }

      case actionTypes.REMOVE_PROJECT:
        // eslint-disable-next-line no-case-declarations
        const updatedProjects: Project[] = state.projects.filter(
          project => project.pUID !== action.project.pUID
        )
        return {
          ...state,
          projects: updatedProjects,
        }
    }
    
    return state
  }
  
  export default reducer