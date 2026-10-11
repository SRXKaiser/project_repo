import type { Proyecto } from '../types';

interface CardProyectoProps{
  proyecto: Proyecto;
  onClick?: (proyecto: Proyecto) => void;
}
const CardProyecto = ({ proyecto, onClick }: CardProyectoProps) => {
  // Formatear fecha
  const fecha = new Date(proyecto.fecha).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

  return (
    <article
      onClick={() => onClick?.(proyecto)}
      className="group cursor-pointer bg-[var(--bg)] border-2 border-[var(--cafe)]
                 border-r-6 border-b-6
                 rounded-lg overflow-hidden shadow-sm hover:shadow-xl
                 transition-all duration-200 hover:-translate-y-1 "
    >
      {/* Imagen / placeholder */}
      <div className="h-40 bg-[var(--rojo-oscuro)]/10 flex items-center justify-center overflow-hidden border-[var(--cafe)] border-b-2">
        {proyecto.imagen ? (
          <img
            src={proyecto.imagen}
            alt={proyecto.titulo}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
          />
        ) : (
          <span className="font-pixel text-4xl text-[var(--rojo-oscuro)]/30">
            📄
          </span>
        )}
      </div>

      {/* Contenido */}
      <div className="p-5">
        {/* Categoría */}
        <span className="inline-block text-xs font-bold uppercase tracking-wide
                         text-[var(--rojo)] bg-[var(--rojo)]/10
                         px-2 py-1 rounded mb-3">
          {proyecto.departamento}
        </span>

        {/* Título */}
        <h3 className="font-pixel text-lg text-[var(--rojo-oscuro)] mb-2 line-clamp-2">
          {proyecto.titulo}
        </h3>

        {/* Autor + fecha */}
        <div className="flex items-center justify-between text-xs text-[var(--cafe)]/80 mb-3">
          <span>👤 {proyecto.autor}</span>
          <span>{fecha}</span>
        </div>

        {/* Resumen */}
        <p className="font-cuerpo text-sm text-[var(--cafe)] line-clamp-3">
          {proyecto.resumen}
        </p>

        {/* Footer */}
        <div className="btn flex items-end justify-between mt-4 pt-3 border-t border-[var(--cafe)]/10">

          <span className="btn-tapa text-xs font-semibold text-[var(--rojo)] group-hover:underline">
            Ver más →
          </span>
        </div>
      </div>
    </article>
  );
};

export default CardProyecto;