import { Link } from 'react-router-dom';

interface DashboardWelcomeProps {
  nombre: string;
}

const DashboardWelcome = ({ nombre }: DashboardWelcomeProps) => {
  return (
    <section className="bg-[var(--rojo-oscuro)] text-[var(--bg)]
                        rounded-2xl p-6 md:p-8
                        flex flex-col md:flex-row md:items-center
                        gap-4 md:gap-6 mb-6">
      <div className="flex-1">
        <h2 className="font-pixel text-2xl md:text-3xl mb-2">
          Bienvenido, {nombre}
        </h2>
        <p className="font-cuerpo text-sm md:text-base text-[var(--bg)]/80 leading-relaxed">
          Desde aquí puedes administrar tus proyectos, consultar su estado y dar
          seguimiento al proceso de revisión y publicación.
        </p>
      </div>

      <Link
        to="/dashboard/crear"
        className="shrink-0 inline-flex items-center justify-center
                   px-5 py-2.5 rounded-lg
                   bg-[var(--bg)] text-[var(--rojo-oscuro)]
                   font-semibold hover:opacity-90 transition"
      >
        + Crear proyecto
      </Link>
    </section>
  );
};

export default DashboardWelcome;