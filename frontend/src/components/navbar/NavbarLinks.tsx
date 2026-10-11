import { Link } from 'react-router-dom';

interface NavbarLink {
  to: string;
  label: string;
}

interface NavbarLinksProps {
  links: NavbarLink[];
  className?: string;
}

// Links por defecto para la página pública
export const LINKS_PUBLICOS: NavbarLink[] = [
  { to: '/#inicio', label: 'INICIO' },
  { to: '/#qnesSomos', label: '¿QUIENES SOMOS?' },
  { to: '/#servicios', label: 'NUESTROS SERVICIOS' },
  { to: '/#contacto', label: 'CONTACTANOS' },
];

const NavbarLinks = ({ links, className = '' }: NavbarLinksProps) => {
  return (
    <ul className={`flex space-x-5 font-cuerpo font-medium text-[var(--cafe)] ${className}`}>
      {links.map((l) => (
        <li
          key={l.to}
          className="hover:underline hover:underline-offset-4
                     hover:text-[var(--rojo)] transition-all duration-100 ease-linear"
        >
          <Link to={l.to}>{l.label}</Link>
        </li>
      ))}
    </ul>
  );
};

export default NavbarLinks;