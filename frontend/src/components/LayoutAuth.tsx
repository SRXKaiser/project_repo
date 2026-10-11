import { Outlet } from "react-router-dom";
import NavbarAuth from "./navbar/NavBarAuth";

const LayoutAuth = () => {
    return (
        <>
        <NavbarAuth />
        <main className="flex-1">
            <Outlet />
        </main>
        </>
    );
};

export default LayoutAuth;