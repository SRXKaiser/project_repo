import { useState, useRef, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface DashboardHeaderProps {
  onMenuClick: () => void;
}

const DashboardHeader = ({ onMenuClick }: DashboardHeaderProps) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  const iniciales = user.name
    .split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();

  return (
    <header className="sticky top-0 z-30 bg-[var(--bg)]/80 backdrop-blur-md
                       border-b border-[var(--cafe)]/20">
      <div className="px-4 lg:px-6 py-3 flex items-center justify-between">
        {/* Botón menú (móvil) */}
        <button
          onClick={onMenuClick}
          className="lg:hidden p-2 rounded-md
                     hover:bg-[var(--rojo)]/10 transition"
          aria-label="Abrir menú"
        >
          <svg className="w-6 h-6 text-[var(--cafe)]" fill="none"
               stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                  d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Espaciador en desktop */}
        <div className="hidden lg:block" />

        {/* Usuario */}
        <div className="relative" ref={ref}>
          <button
            onClick={() => setOpen(!open)}
            className="flex items-center gap-3 px-2 py-1.5 rounded-lg
                       hover:bg-[var(--rojo)]/5 transition"
          >
            <div className="w-9 h-9 rounded-full bg-[var(--rojo)] text-[var(--bg)]
                            flex items-center justify-center
                            font-bold text-sm">
              {iniciales}
            </div>

            <div className="hidden md:flex flex-col items-start">
              <strong className="text-sm text-[var(--text-h)] font-cuerpo">
                {user.name}
              </strong>
              <span className="text-xs text-[var(--cafe)]/70">
                {user.role}
              </span>
            </div>

            <svg className={`w-4 h-4 text-[var(--cafe)] transition-transform
                             ${open ? 'rotate-180' : ''}`}
                 fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" strokeLinecap="round"
                    strokeWidth="2" d="m19 9-7 7-7-7" />
            </svg>
          </button>

          {/* Dropdown */}
          {open && (
            <div className="absolute right-0 mt-2 z-30 w-56
                            bg-[var(--bg)] border border-[var(--cafe)]/20
                            rounded-lg shadow-xl p-2">
              <Link
                to="/dashboard/perfil"
                onClick={() => setOpen(false)}
                className="block px-3 py-2 rounded-md text-sm text-[var(--cafe)]
                           hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
              >
                Mi perfil
              </Link>
              <Link
                to="/dashboard/configuracion"
                onClick={() => setOpen(false)}
                className="block px-3 py-2 rounded-md text-sm text-[var(--cafe)]
                           hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
              >
                Configuración
              </Link>
              <button
                onClick={handleLogout}
                className="w-full text-left px-3 py-2 rounded-md text-sm
                           text-[var(--rojo)] font-semibold
                           hover:bg-[var(--rojo)]/10 transition mt-1"
              >
                Cerrar sesión
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default DashboardHeader;