import NavbarLogo from "./NavBarLogo";

interface NavbarAuthProps {
  slogan?: string;
}

const NavbarAuth = ({
  slogan = 'Repositorio Institucional de Investigación',
}: NavbarAuthProps) => {
  return (
    <nav className="fixed top-0 left-0 w-full z-50 bg-[var(--bg)]
                    border-b border-[var(--cafe)]">
      <div className="px-8 py-3 flex justify-between items-center">
        <NavbarLogo />

        <p className="font-pixel text-sm md:text-base text-[var(--cafe)] italic">
          {slogan}
        </p>
      </div>
    </nav>
  );
};

export default NavbarAuth;