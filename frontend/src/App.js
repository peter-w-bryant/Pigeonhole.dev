import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css'

import Layout from './components/Layout'
import Home from './components/Home'
import NotFound from './components/NotFound'
import Registration from './components/Registration';
import Profile from './components/Profile';

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path='/' element={<Layout />}>
                        <Route index element={<Home />} />
                        <Route path='profile' element={<Profile />} />
                        <Route path='registration' element={<Registration />} />
                        <Route path='*' element={<NotFound />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </>
    );
}

export default App;