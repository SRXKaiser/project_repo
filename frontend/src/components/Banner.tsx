import { Link, useNavigate, useLocation } from 'react-router-dom';
const Banner = () => {
    return (
        <div className="fixed bottom-0 left-0 w-full z-40 bg-[var(--rojo-oscuro)] shadow-2xl">
            <div className="p-6 pb-10 ml-20 mr-30 flex justify-between items-center gap-6">
                <div>
                    <h2 className="text-left text-[var(--bg)] font-pixel">
                        ¿Formas parte de la comunidad ITCJ?
                    </h2>
                    <p className="text-left text-[var(--bg)] font-pixel ">
                        InvestigaTec: comparte tus proyectos, descubre nuevas áreas. Regístrate hoy.
                    </p>
                </div>

                <div >
                    <Link
                        to="/register"
                        className="btn flex items-center justify-center  justify-end rounded px-6 py-2.5 font-semibold hover:shadow-lg hover:text-[var(--rojo)] transition duration-200"
                    >
                        <span className="btn-tapa font-pixel font-bold text-[18px]">CREA UNA CUENTA</span>
                    </Link>
                </div>

            </div>
        </div>
    );
};

export default Banner;