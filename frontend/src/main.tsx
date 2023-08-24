import ReactDOM from 'react-dom/client'

import { createStore, applyMiddleware, Store } from "redux"
import { Provider } from "react-redux"
import thunk from "redux-thunk"

import App from './App.tsx'
import reducer from "./store/reducer"

import './index.css'
import 'bootstrap/dist/css/bootstrap.min.css';

const store: Store<ProjectState, ProjectAction> & {
  dispatch: DispatchType
} = createStore(reducer, applyMiddleware(thunk))

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Provider store={store}>
    <App />
  </Provider>,
)
