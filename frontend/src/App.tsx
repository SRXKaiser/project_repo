import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Layout from './components/Layout';
import LayoutAuth from './components/LayoutAuth';
import Home from './pages/Home';
import ScrollToHash from './components/ScrollTohash';
import Explorar from './pages/Explorar';
import Login from './pages/Login';
import Register from './pages/Register';
// import './App.css'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <AuthProvider>
      <BrowserRouter>
      <ScrollToHash />
         <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/explorar" element={<Explorar />} />
            
          </Route>
          <Route element={<LayoutAuth />}>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider >
  )
}

export default App
