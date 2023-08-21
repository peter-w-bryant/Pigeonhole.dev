import * as actionTypes from './actionTypes'

export function addProject(project: Project) {
    const action: ProjectAction = {
        type: actionTypes.ADD_PROJECT,
        project,
    }

    return dispatch(action)
}

export function removeProject(project: Project) {
    const action: ProjectAction = {
      type: actionTypes.REMOVE_PROJECT,
      project,
    }
    
    return dispatch(action)
}

export function dispatch(action: ProjectAction) {
    return (dispatch: DispatchType) => {
        dispatch(action)
    }
}