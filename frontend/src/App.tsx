import { useState } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import LayoutAuth from './components/LayoutAuth';
import Home from './pages/Home';
import ScrollToHash from './components/ScrollTohash';
import Explorar from './pages/Explorar';
import Login from './pages/Login';
import Register from './pages/Register';
import DashboardUser from './pages/DashBoard-User';
import DashboardAdmin from './pages/DashBoard-Admin';
import DashboardLayout from './components/user-dashboard/DBLayout';
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

          <Route
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard-user" element={<DashboardUser />} />
            <Route path="/dashboard-admin" element={<DashboardAdmin />} />
          </Route>
          
          
        </Routes>
      </BrowserRouter>
    </AuthProvider >
  )
}

export default App
