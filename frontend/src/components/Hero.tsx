

const Hero = () => {
  return (
    <section
      id="inicio"
      className="full-bleed grid grid-cols-2 gap-2 pr-36 pl-36 pt-2 mb-2  overflow-hidden"
    >
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-4 animate-caer drop-shadow-lg">
          Repositorio Institucional de Proyectos de Investigación
        </h1>

        <p className=" mb-3 font-sub-pixel text-justify">
          Explora, comparte y consulta los proyectos de investigación de nuestra universidad. Todo en un solo lugar.
        </p>

        
      </div>

      <div className="bg-[url(/src/assets/biblioteca.png)] bg-center bg-no-repeat bg-contain hover:animate-swing hover:origin-top min-h-[300px] mt-2"></div>
    </section>
  );
};

export default Hero;