import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { Usuario } from '../types';

// ─── Forma del contexto ───
interface AuthContextValue {
  user: Usuario | null;
  login: (user: Usuario, token: string) => void;
  logout: () => void;
  loading: boolean;
}

// ─── Contexto con tipo ───
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// ─── Usuario mock temporal (quitar cuando haya backend) ───
const USUARIO_MOCK: Usuario = {
  id: 1,
  name: 'Ana Martínez',
  email: 'ana@itcj.edu.mx',
  role: 'estudiante',
};

// ─── Provider ───
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  // ⚠️ TEMPORAL: inicializamos con el mock para que el dashboard funcione
  const [user, setUser] = useState<Usuario | null>(USUARIO_MOCK);
  const [loading, setLoading] = useState(false);   // ← ya no está comentado

  // ─── Recuperar usuario del localStorage (cuando tengas backend) ───
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');

    if (storedUser && token) {
      try {
        setUser(JSON.parse(storedUser));
      } catch {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    // ⚠️ NO ponemos el mock aquí porque ya está en useState
    // Cuando tengas backend, cambia el useState inicial a `null` y descomenta el mock por defecto:
    // else { setUser(USUARIO_MOCK); }
  }, []);

  const login = (userData: Usuario, token: string) => {
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

// ─── Hook con verificación ───
export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe usarse dentro de <AuthProvider>');
  }
  return context;
};