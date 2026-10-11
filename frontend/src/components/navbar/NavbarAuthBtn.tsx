import { Link } from 'react-router-dom';

const NavbarAuthButtons = () => {
  return (
    <>
      <Link
        to="/register"
        className="btn flex items-center justify-center rounded
                   px-6 py-2.5 font-semibold
                   hover:shadow-lg hover:text-[var(--rojo)] transition duration-200"
      >
        <span className="btn-tapa">REGISTRATE</span>
      </Link>
      <Link
        to="/login"
        className="btn flex items-center justify-center rounded-md
                   bg-[var(--rojo)] text-[var(--bg)] px-6 py-2.5
                   font-semibold hover:shadow-lg hover:bg-[var(--azul)] transition duration-200"
      >
        <span className="btn-tapa">INICIAR SESIÓN</span>
      </Link>
    </>
  );
};

export default NavbarAuthButtons;