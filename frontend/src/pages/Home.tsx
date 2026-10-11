import { Link } from 'react-router-dom';
import { servicios, razonesCajaAzul } from '../data/homeContent';
import CardService from '../components/CardService';
import BlueBox from '../components/BlueBox';
import Separador from '../components/Separador';
import separador from '../assets/separador.png';
import separador2 from '../assets/separador2.png';
import Hero from '../components/Hero';

const Home = () => {
  return (
    <div className="relative max-w-7xl mx-auto px-4 py-12">
      <Hero />
      <div className=" justify-center mb-10 pt-5 w-full">
        <Link
            to="/explorar"
            className="btn flex items-center justify-center rounded px-6 py-2.5 font-semibold hover:shadow-lg hover:text-[var(--rojo)] transition duration-200"
          >
            <span className="btn-tapa font-pixel">Empieza a explorar proyectos y conéctate con el saber</span>
          </Link>
      </div>

      <Separador src={separador} />

      <section id='qnesSomos'>
        <div className="full-bleed bg-[url('/src/assets/fondo.png')] p-10 bg-cover">
          <section className="m-30 p-15 bg-[var(--azul)] grid grid-cols-2 gap-2">
            <div className="bg-[url('/src/assets/Estrella.png')] bg-no-repeat bg-center bg-contain flex items-center justify-center hover:animate-swing hover:origin-top w-80 h-80">
              <h2 className="text-[var(--bg)] leading-tight font-cuerpo text-center text-2xl font-bold max-w-[60%]">
                El conocimiento no debería ser olvidado
              </h2>
            </div>

            <p className="text-[var(--bg)] text-justify m-8 font-semibold">En el Instituto Tecnológico de Ciudad Juárez, la investigación académica y científica avanza… pero lo hace en islas separadas.

              Cada departamento guarda sus proyectos como tesoros invisibles: archivos aislados, sin conexión, sin memoria compartida. El resultado es inevitable: proyectos olvidados, esfuerzos duplicados y una comunidad que no puede ver todo lo que es capaz de crear.
            </p>



          </section>
        </div>

        <Separador src={separador2} />

        <section className='relative'>
          <div className='sticky top-0 h-screen flex flex-col justify-center items-center z-0 pointer-events-none px-8 mr-50 ml-50 mt-3 mb-30'>
            <h1 className=' p-10 text-center text-[var(--bg)] bg-[var(--rojo)] font-cuerpo font-bold leading-15 max-w-4xl'>
              Cuando la información no fluye, nadie encuentra lo que ya existe.
            </h1>
            <p className='text-xl text-center text-[var(--cafe)] font-sub-pixel font-semibold max-w-2xl mt-4'>
              Se pierden conexiones, colaboraciones y el progreso que solo nace del encuentro entre disciplinas.
            </p>
          </div>
          <div className='relative z-10 -mt-[100vh] grid grid-cols-2 grid-rows-4 gap-6 font-sub-pixel text-[var(--cafe)] pt-[50vh] pb-[50vh] px-20'>
            {razonesCajaAzul.map((p) => (
              <BlueBox key={p.id} texto={p.texto} align={p.align} />
            ))}
          </div>
        </section>

        <section>
          <div className="full-bleed bg-[url('/src/assets/fondorayas.png')] p-10 bg-cover">
            <div className='border-3 rounded-md border-[var(--cafe)] border-dashed bg-[var(--bg)] p-15 m-30'>
              <h2 className="text-[var(--cafe)] font-pixel text-left text-2xl font-bold ">
                La respuesta:
              </h2>
              <h1 className="text-4xl font-bold text-[var(--cafe)] text-left">
                Un repositorio centralizado
              </h1>
              <p className='text-xl text-left text-[var(--cafe)] font-sub-pixel font-semibold '>
                Imagina toda la producción académica del ITCJ en un solo lugar.
                Accesible. Consultable. Viva.
              </p>
              <p className='text-m text-left text-[var(--cafe)] font-sub-pixel font-semibold max-w-2xl mt-4'>
                Eso es exactamente lo que propone este proyecto: consolidar, preservar y compartir el conocimiento que hoy está disperso. Una única plataforma donde estudiantes, docentes e investigadores puedan descubrir, reutilizar y conectar el saber que se genera dentro del instituto.
              </p>
            </div>
          </div>
        </section>
      </section>


      <section id='servicios' className='mb-20'>
        <h1 className='text-8xl font-bold font-sub-pixel text-[var(--rojo-oscuro)] pt-20'>
          Servicios
        </h1>
        <div className='servicios-palette ml-5 mr-5 grid grid-cols-3 gap-2'>
          {servicios.map((servicio) => (
            <CardService key={servicio.id} {...servicio} />
          ))}
        </div>
      </section>

      <Separador src={separador} />

      <section className="m-5">
        <div>
          <h1 className="text-2xl font-bold text-[var(--rojo-oscuro)] mb-0">
            Es asi de simple!
          </h1>
          <p className=" font-bold text-[var(--rojo-oscuro)] font-sub-pixel">
            Unete y comienza a compartir tus investigaciones y encuentra nuevos investigaciones
          </p>
          <div className='content-center justify-items-center m-10'>
            <img className='w-80' src="/src/assets/cat-thumbs-up.gif" alt="" />
          </div>

        </div>
        <div className="grid grid-cols-2 gap-6 mr-30 ml-30 mt-5">
          <Link
            to="/explorar"
            className="btn flex items-center justify-center rounded px-6 py-2.5 font-semibold hover:shadow-lg hover:text-[var(--rojo)] transition duration-200"
          >
            <span className="btn-tapa">VER PROYECTOS</span>
          </Link>
          <Link
            to="/publicar"
            className="btn flex items-center justify-center rounded-md bg-[var(--rojo)] text-[var(--bg)] px-6 py-2.5 font-semibold hover:shadow-lg hover:bg-[var(--azul)] transition duration-200"
          >
            <span className="btn-tapa">PUBLICAR</span>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;