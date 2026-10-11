import type { EstadisticasDashboard } from '../../types';

interface DashboardStatsProps {
  stats: EstadisticasDashboard;
}

const DashboardStats = ({ stats }: DashboardStatsProps) => {
  const items = [
    { icon: 'PR', valor: stats.totalProyectos, label: 'Mis proyectos' },
    { icon: 'BR', valor: stats.borradores, label: 'Borradores' },
    { icon: 'RV', valor: stats.enRevision, label: 'En revisión' },
    { icon: 'PB', valor: stats.publicados, label: 'Publicados' },
  ];

  return (
    <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {items.map((item) => (
        <article
          key={item.label}
          className="bg-[var(--bg)] border border-[var(--cafe)]/20
                     rounded-xl p-5 flex flex-col gap-2
                     hover:shadow-md transition-shadow"
        >
          <span className="w-9 h-9 rounded-md bg-[var(--rojo)]/10
                           text-[var(--rojo)] text-xs font-bold
                           flex items-center justify-center">
            {item.icon}
          </span>
          <strong className="font-pixel text-3xl text-[var(--rojo-oscuro)]">
            {item.valor}
          </strong>
          <span className="font-cuerpo text-sm text-[var(--cafe)]">
            {item.label}
          </span>
        </article>
      ))}
    </section>
  );
};

export default DashboardStats;