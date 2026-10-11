import { Link } from 'react-router-dom';

interface NavbarLogoProps {
  variant?: 'default' | 'small';
}

const NavbarLogo = ({ variant = 'default' }: NavbarLogoProps) => {
  const size = variant === 'small' ? 'text-xl' : 'text-2xl';

  return (
    <Link
      to="/"
      className={`${size} font-pixel hover:text-[var(--rojo-oscuro)] transition-all duration-100`}
    >
      <h2>
        <span>Investiga</span>
        <span className="text-[var(--rojo)]">Tec</span>
      </h2>
    </Link>
  );
};

export default NavbarLogo;