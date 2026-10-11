interface CardServiceProps {
  titulo: string;
  subtitulo: string;
  descripcion: string;
}

const CardService = ({titulo, subtitulo, descripcion}: CardServiceProps) => (
    

<div className='servicio-card bg-[var(--rojo-oscuro)] text-[var(--bg)] p-5 m-5'>
            <h2 className="servicio-titulo text-[var(--bg)] font-pixel text-2xl font-bold ">
              {titulo}
            </h2>
            <p className='servicio-subtitulo text-xl text-justify text-[var(--bg)] font-sub-pixel font-semibold '>
              {subtitulo}
            </p>
            <p className='servicio-descripcion text-justify text-[var(--bg)] font-sub-pixel font-semibold max-w-2xl mt-4'>
              {descripcion}
            </p>
</div>

);

export default CardService;