import type { Actividad } from '../../types';

interface DashboardActivityProps {
  actividades: Actividad[];
}

const DashboardActivity = ({ actividades }: DashboardActivityProps) => {
  return (
    <aside className="bg-[var(--bg)] border border-[var(--cafe)]/20
                      rounded-xl p-5">
      <h2 className="font-pixel text-lg text-[var(--rojo-oscuro)] mb-4">
        Actividad reciente
      </h2>

      <div className="flex flex-col gap-4">
        {actividades.map((a) => (
          <div key={a.id} className="flex gap-3">
            <span className="w-2 h-2 rounded-full bg-[var(--rojo)]
                             mt-2 shrink-0" />
            <div className="flex flex-col min-w-0">
              <strong className="font-cuerpo text-sm text-[var(--text-h)]">
                {a.titulo}
              </strong>
              <span className="text-xs text-[var(--cafe)]/70 truncate">
                {a.descripcion}
              </span>
            </div>
          </div>
        ))}

        {actividades.length === 0 && (
          <p className="text-sm text-[var(--cafe)]/70 text-center py-4">
            Sin actividad reciente.
          </p>
        )}
      </div>
    </aside>
  );
};

export default DashboardActivity;