import { Link } from 'react-router-dom';
import type { ProyectoDashboard, EstadoProyecto } from '../../types';

interface DashboardProjectsProps {
  proyectos: ProyectoDashboard[];
}

// Estilos por estado
const estiloEstado = (estado: EstadoProyecto) => {
  switch (estado) {
    case 'Borrador':
      return 'bg-[var(--cafe)]/10 text-[var(--cafe)]';
    case 'En revisión':
      return 'bg-amber-500/15 text-amber-700';
    case 'Publicado':
      return 'bg-green-500/15 text-green-700';
    case 'Archivado':
      return 'bg-gray-500/15 text-gray-700';
  }
};

const DashboardProjects = ({ proyectos }: DashboardProjectsProps) => {
  return (
    <article className="bg-[var(--bg)] border border-[var(--cafe)]/20
                        rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-pixel text-lg text-[var(--rojo-oscuro)]">
          Mis proyectos recientes
        </h2>
        <Link
          to="/dashboard/mis-proyectos"
          className="text-sm text-[var(--cafe)] hover:text-[var(--rojo)] transition"
        >
          Ver todos →
        </Link>
      </div>

      <div className="flex flex-col divide-y divide-[var(--cafe)]/10">
        {proyectos.map((p) => (
          <Link
            key={p.id}
            to={`/proyecto/${p.id}`}
            className="flex items-center justify-between gap-4 py-3
                       hover:bg-[var(--rojo)]/5 -mx-2 px-2 rounded transition"
          >
            <div className="flex flex-col min-w-0">
              <h3 className="font-cuerpo font-semibold text-[var(--text-h)]
                             truncate">
                {p.titulo}
              </h3>
              <span className="text-xs text-[var(--cafe)]/70">
                {p.areaTematica} · Actualizado recientemente
              </span>
            </div>

            <span className={`shrink-0 text-xs font-bold px-2.5 py-1 rounded-full
                             ${estiloEstado(p.estado)}`}>
              {p.estado}
            </span>
          </Link>
        ))}

        {proyectos.length === 0 && (
          <p className="text-sm text-[var(--cafe)]/70 py-4 text-center">
            No tienes proyectos aún.
          </p>
        )}
      </div>
    </article>
  );
};

export default DashboardProjects;