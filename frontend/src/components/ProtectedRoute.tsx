import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: ReactNode;
  requiereAdmin?: boolean;
}

const ProtectedRoute = ({
  children,
  requiereAdmin = false,
}: ProtectedRouteProps) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Cargando...</p>
      </div>
    );
  }

  if (!user) {
    return (
      <Navigate
        to="/login"
        state={{ from: location.pathname + location.search }}
        replace
      />
    );
  }

  if (requiereAdmin && !user.es_administrador) {
    return <Navigate to="/dashboard-user" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;