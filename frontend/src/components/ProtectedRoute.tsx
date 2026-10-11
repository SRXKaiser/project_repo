import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

interface ProtectedRouteProps {
    children: ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const {user, loading} = useAuth();

    if (loading) return <div className="text-center py-10">Cargando</div>
    if (!user) return <Navigate to="/login" replace />;

    return children;
};

export default ProtectedRoute;