import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import NavbarLogo from './NavBarLogo';
import NavbarLinks, { LINKS_PUBLICOS } from './NavbarLinks';
import NavbarAuthButtons from './NavbarAuthBtn';
import NavbarUserMenu from './NavbarUser';
import NavbarMobileMenu from './NavbarMobile';

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', handleScroll);
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

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
          <NavbarLogo />

          <div className="hidden lg:block">
            <NavbarLinks links={LINKS_PUBLICOS} />
          </div>

          <div className="flex gap-4 items-center">
            <div className="hidden lg:flex lg:items-center gap-x-2">
              {user ? <NavbarUserMenu /> : <NavbarAuthButtons />}
            </div>

            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="flex items-center justify-center lg:hidden p-2
                         rounded-md hover:bg-[var(--rojo)]/10 transition"
              aria-label={menuOpen ? 'Cerrar menú' : 'Abrir menú'}
            >
              {menuOpen ? (
                <svg className="w-7 h-7 text-[var(--cafe)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18 18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-7 h-7 text-[var(--cafe)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </nav>

      <NavbarMobileMenu open={menuOpen} onClose={() => setMenuOpen(false)} />
    </>
  );
};

export default Navbar;