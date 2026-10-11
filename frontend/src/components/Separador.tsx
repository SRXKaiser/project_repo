import separadorDefault from '../assets/separador.png';

const Separador = ({ src = separadorDefault, height = 'h-28' }) => (
  <div className="full-bleed">
    <img
      src={src}
      alt=""
      className={`w-full ${height} object-cover`}
    />
  </div>
);

export default Separador;