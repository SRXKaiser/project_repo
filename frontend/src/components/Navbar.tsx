import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface NavbarLink {
  to: string;
  label: string;
}

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Detectar scroll
  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Cerrar menú al cambiar de ruta
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  // Bloquear scroll del body cuando el menú está abierto
  useEffect(() => {
    document.body.style.overflow = menuOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [menuOpen]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const links: NavbarLink[] = [
    { to: '/#inicio', label: 'INICIO' },
    { to: '/#qnesSomos', label: '¿QUIENES SOMOS?' },
    { to: '/#servicios', label: 'NUESTROS SERVICIOS' },
    { to: '/#contacto', label: 'CONTACTANOS' },
  ];

  return (
    <>
      <nav
        className={`
          fixed top-0 left-0 w-full z-50
          border-b border-[var(--cafe)]
          transition-colors duration-300 
          ${scrolled ? 'bg-[var(--bg)]/50 backdrop-blur-md' : 'bg-[var(--bg)]'}
        `}
      >
        <div className="px-8 py-3 flex justify-between items-center">
          {/* LOGO */}
          <Link
            to="/"
            className="text-2xl font-pixel hover:text-[var(--rojo-oscuro)] transition-all duration-100"
          >
            <h2>
              <span>Investiga</span>
              <span className="text-[var(--rojo)]">Tec</span>
            </h2>
          </Link>

          {/* LINKS (desktop) */}
          <div className="hidden lg:block">
            <ul className="flex space-x-5 font-cuerpo font-medium text-[var(--cafe)]">
              {links.map((l) => (
                <li
                  key={l.to}
                  className="hover:underline hover:underline-offset-4 hover:text-[var(--rojo)] transition-all duration-100 ease-linear"
                >
                  <Link to={l.to}>{l.label}</Link>
                </li>
              ))}
            </ul>
          </div>

          {/* BOTONES (desktop) */}
          <div className="flex gap-4 items-center">
            <div className="hidden lg:flex lg:items-center gap-x-2">
              <Link
                to="/register"
                className="btn flex items-center justify-center rounded px-6 py-2.5 font-semibold hover:shadow-lg hover:text-[var(--rojo)] transition duration-200"
              >
                <span className="btn-tapa">REGISTRATE</span>
              </Link>
              <Link
                to="/login"
                className="btn flex items-center justify-center rounded-md bg-[var(--rojo)] text-[var(--bg)] px-6 py-2.5 font-semibold hover:shadow-lg hover:bg-[var(--azul)] transition duration-200"
              >
                <span className="btn-tapa">INICIAR SESIÓN</span>
              </Link>
            </div>

            {/* HAMBURGUESA (móvil) */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="flex items-center justify-center lg:hidden p-2 rounded-md hover:bg-[var(--rojo)]/10 transition"
              aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
            >
              {menuOpen ? (
                /* Ícono X */
                <svg
                  className="w-7 h-7 text-[var(--cafe)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18 18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                /* Ícono hamburguesa */
                <svg
                  className="w-7 h-7 text-[var(--cafe)]"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </nav>

      {/* ─── MENÚ MÓVIL ─── */}
      {menuOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          {/* Fondo oscuro */}
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMenuOpen(false)}
          />

          {/* Panel deslizante desde la derecha */}
          <div
            className="absolute top-0 right-0 h-full w-72 max-w-full
                       bg-[var(--bg)] shadow-2xl
                       flex flex-col
                       animate-slide-in"
          >
            {/* Header del panel */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--cafe)]/20 mt-16">
              <span className="font-pixel text-lg text-[var(--rojo-oscuro)]">
                Menú
              </span>
            </div>

            {/* Links */}
            <ul className="flex flex-col p-4 gap-1 font-cuerpo font-medium text-[var(--cafe)]">
              {links.map((l) => (
                <li key={l.to}>
                  <Link
                    to={l.to}
                    onClick={() => setMenuOpen(false)}
                    className="block px-4 py-3 rounded-md hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>

            {/* Botones de auth */}
            <div className="mt-auto p-4 border-t border-[var(--cafe)]/20 flex flex-col gap-2">
              {user ? (
                <button
                  onClick={handleLogout}
                  className="w-full px-4 py-3 rounded-md bg-[var(--rojo)] text-[var(--bg)] font-semibold hover:bg-[var(--azul)] transition"
                >
                  Cerrar sesión
                </button>
              ) : (
                <>
                  <Link
                    to="/register"
                    onClick={() => setMenuOpen(false)}
                    className="w-full text-center px-4 py-3 rounded-md border border-[var(--cafe)]/30 text-[var(--cafe)] font-semibold hover:bg-[var(--rojo)]/10 transition"
                  >
                    Regístrate
                  </Link>
                  <Link
                    to="/login"
                    onClick={() => setMenuOpen(false)}
                    className="w-full text-center px-4 py-3 rounded-md bg-[var(--rojo)] text-[var(--bg)] font-semibold hover:bg-[var(--azul)] transition"
                  >
                    Iniciar sesión
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;