import { useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import NavbarLinks, { LINKS_PUBLICOS } from './NavbarLinks';
import NavbarAuthButtons from './NavbarAuthBtn';

interface NavbarMobileMenuProps {
  open: boolean;
  onClose: () => void;
}

const NavbarMobileMenu = ({ open, onClose }: NavbarMobileMenuProps) => {
  const location = useLocation();

  // Cerrar al cambiar de ruta
  useEffect(() => {
    onClose();
  }, [location.pathname, onClose]);

  // Bloquear scroll del body
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [open]);

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-40 lg:hidden">
      <div className="absolute inset-0 bg-black/40" onClick={onClose} />

      <div className="absolute top-0 right-0 h-full w-72 max-w-full
                      bg-[var(--bg)] shadow-2xl
                      flex flex-col animate-slide-in">
        <div className="flex items-center justify-between px-6 py-4
                        border-b border-[var(--cafe)]/20 mt-16">
          <span className="font-pixel text-lg text-[var(--rojo-oscuro)]">
            Menú
          </span>
        </div>

        <ul className="flex flex-col p-4 gap-1 font-cuerpo font-medium text-[var(--cafe)]">
          {LINKS_PUBLICOS.map((l) => (
            <li key={l.to}>
              <Link
                to={l.to}
                onClick={onClose}
                className="block px-4 py-3 rounded-md
                           hover:bg-[var(--rojo)]/10 hover:text-[var(--rojo)] transition"
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="mt-auto p-4 border-t border-[var(--cafe)]/20 flex flex-col gap-2">
          <NavbarAuthButtons />
        </div>
      </div>
    </div>
  );
};

export default NavbarMobileMenu;