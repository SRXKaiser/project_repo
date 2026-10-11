import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface SidebarLink {
  to: string;
  label: string;
  icon: string;
}

const LINKS_MI_ESPACIO: SidebarLink[] = [
  { to: '/dashboard', label: 'Inicio', icon: 'IN' },
  { to: '/dashboard/mis-proyectos', label: 'Mis proyectos', icon: 'MP' },
  { to: '/dashboard/crear', label: 'Crear proyecto', icon: '+' },
  { to: '/explorar', label: 'Explorar', icon: 'EX' },
];

const LINKS_CUENTA: SidebarLink[] = [
  { to: '/dashboard/perfil', label: 'Mi perfil', icon: 'PE' },
];

interface DashboardSidebarProps {
  open: boolean;
  onClose: () => void;
}

const DashboardSidebar = ({ open, onClose }: DashboardSidebarProps) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-cuerpo
     transition-colors duration-150
     ${isActive
       ? 'bg-[var(--rojo)]/15 text-[var(--rojo)] font-semibold'
       : 'text-[var(--cafe)] hover:bg-[var(--rojo)]/5 hover:text-[var(--rojo)]'
     }`;

  return (
    <>
      {/* Overlay en móvil */}
      {open && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-full w-64 z-50
          bg-[var(--bg)] border-r border-[var(--cafe)]/20
          flex flex-col
          transition-transform duration-300
          ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
      >
        {/* Logo */}
        <div className="px-6 py-5 border-b border-[var(--cafe)]/20">
          <span className="font-pixel text-xl">
            <span>Investiga</span>
            <span className="text-[var(--rojo)]">Tec</span>
          </span>
        </div>

        {/* Links */}
        <nav className="flex-1 overflow-y-auto p-4 flex flex-col gap-6">
          {/* Mi espacio */}
          <div>
            <span className="block text-xs uppercase tracking-wide
                             text-[var(--cafe)]/60 font-bold px-3 mb-2">
              Mi espacio
            </span>
            <div className="flex flex-col gap-1">
              {LINKS_MI_ESPACIO.map((l) => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  end={l.to === '/dashboard'}
                  onClick={onClose}
                  className={linkClasses}
                >
                  <span className="w-7 h-7 rounded-md bg-[var(--cafe)]/10
                                   flex items-center justify-center
                                   text-[10px] font-bold">
                    {l.icon}
                  </span>
                  {l.label}
                </NavLink>
              ))}
            </div>
          </div>

          {/* Cuenta */}
          <div>
            <span className="block text-xs uppercase tracking-wide
                             text-[var(--cafe)]/60 font-bold px-3 mb-2">
              Cuenta
            </span>
            <div className="flex flex-col gap-1">
              {LINKS_CUENTA.map((l) => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  onClick={onClose}
                  className={linkClasses}
                >
                  <span className="w-7 h-7 rounded-md bg-[var(--cafe)]/10
                                   flex items-center justify-center
                                   text-[10px] font-bold">
                    {l.icon}
                  </span>
                  {l.label}
                </NavLink>
              ))}

              <button
                onClick={handleLogout}
                className="flex items-center gap-3 px-3 py-2.5 rounded-md
                           text-sm font-cuerpo text-[var(--cafe)]
                           hover:bg-[var(--rojo)]/5 hover:text-[var(--rojo)]
                           transition-colors duration-150 text-left"
              >
                <span className="w-7 h-7 rounded-md bg-[var(--cafe)]/10
                                 flex items-center justify-center
                                 text-[10px] font-bold">
                  SA
                </span>
                Cerrar sesión
              </button>
            </div>
          </div>
        </nav>
      </aside>
    </>
  );
};

export default DashboardSidebar;