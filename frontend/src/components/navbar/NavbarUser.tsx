import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const NavbarUserMenu = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Cerrar al hacer clic fuera
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

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 px-3 py-2 rounded-md
                   hover:bg-[var(--rojo)]/10 transition-colors"
      >
        {/* Avatar */}
        <div className="w-8 h-8 rounded-full bg-[var(--rojo)] text-[var(--bg)]
                        flex items-center justify-center font-bold text-sm">
          {user.name.charAt(0).toUpperCase()}
        </div>
        <span className="font-cuerpo text-sm text-[var(--cafe)] hidden md:block">
          {user.name}
        </span>
        <svg
          className={`w-4 h-4 text-[var(--cafe)] transition-transform ${open ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
        >
          <path stroke="currentColor" strokeLinecap="round" strokeWidth="2" d="m19 9-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 mt-2 z-30 min-w-[200px]
                        bg-[var(--bg)] border border-[var(--cafe)]/20
                        rounded-lg shadow-xl p-2">
          <div className="px-3 py-2 border-b border-[var(--cafe)]/20 mb-1">
            <p className="text-sm font-semibold text-[var(--rojo-oscuro)] truncate">
              {user.name}
            </p>
            <p className="text-xs text-[var(--cafe)]/70 truncate">
              {user.email}
            </p>
          </div>

          <Link
            to="/dashboard"
            onClick={() => setOpen(false)}
            className="block px-3 py-2 rounded-md text-sm text-[var(--cafe)]
                       hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
          >
            Dashboard
          </Link>
          <Link
            to="/perfil"
            onClick={() => setOpen(false)}
            className="block px-3 py-2 rounded-md text-sm text-[var(--cafe)]
                       hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
          >
            Mi perfil
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
  );
};

export default NavbarUserMenu;