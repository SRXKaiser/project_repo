import { useParams, Link } from 'react-router-dom';
import { proyectosContent } from '../data/proyectosContent';

const ProyectoDetalle = () => {
  const { id } = useParams<{ id: string }>();
  const proyecto = proyectosContent.find((p) => p.id === Number(id));

  // ─── Proyecto no encontrado ───
  if (!proyecto) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <h1 className="font-pixel text-4xl text-[var(--rojo-oscuro)] mb-4">
          Proyecto no encontrado
        </h1>
        <p className="font-cuerpo text-[var(--cafe)] mb-6">
          El proyecto que buscas no existe o fue eliminado.
        </p>
        <Link
          to="/explorar"
          className="inline-block px-6 py-2.5 rounded-md
                     bg-[var(--rojo)] text-[var(--bg)]
                     font-semibold hover:bg-[var(--azul)] transition"
        >
          Volver a explorar
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      {/* ─── Breadcrumb ─── */}
      <nav className="flex items-center gap-2 text-sm font-cuerpo
                      text-[var(--cafe)]/70 mb-6">
        <Link to="/" className="hover:text-[var(--rojo)] transition">
          Inicio
        </Link>
        <span>›</span>
        <Link to="/explorar" className="hover:text-[var(--rojo)] transition">
          Proyectos
        </Link>
        <span>›</span>
        <span className="text-[var(--rojo-oscuro)] font-semibold">
          Detalle
        </span>
      </nav>

      {/* ─── Grid: contenido + sidebar ─── */}
      <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6">
        
        {/* ═══════ CONTENIDO PRINCIPAL ═══════ */}
        <article className="bg-[var(--bg)] border border-[var(--cafe)]/20
                            rounded-2xl p-6 md:p-8">
          
          {/* Badge de materia */}
          <span className="inline-block text-xs font-bold uppercase tracking-wide
                           text-[var(--rojo)] bg-[var(--rojo)]/10
                           px-3 py-1 rounded mb-4">
            {proyecto.materia}
          </span>

          {/* Título */}
          <h1 className="font-pixel text-3xl md:text-4xl text-[var(--rojo-oscuro)]
                         mb-4 leading-tight">
            {proyecto.titulo}
          </h1>

          {/* Meta */}
          <div className="flex flex-wrap gap-4 text-sm font-cuerpo
                          text-[var(--cafe)]/80 mb-6">
            <span>Estado: <strong>Publicado</strong></span>
            <span>Publicado en <strong>{new Date(proyecto.fecha).getFullYear()}</strong></span>
            <span><strong>{proyecto.departamento}</strong></span>
          </div>

          {/* ─── Resumen ─── */}
          <section className="mb-8">
            <h2 className="font-pixel text-xl text-[var(--rojo-oscuro)] mb-3">
              Resumen
            </h2>
            <p className="font-cuerpo text-[var(--cafe)] leading-relaxed">
              {proyecto.resumen}
            </p>
          </section>

          {/* ─── Áreas temáticas ─── */}
          {proyecto.palabrasClave?.length > 0 && (
            <section className="mb-8">
              <h2 className="font-pixel text-xl text-[var(--rojo-oscuro)] mb-3">
                Áreas temáticas
              </h2>
              <div className="flex flex-wrap gap-2">
                {proyecto.palabrasClave.map((area) => (
                  <span
                    key={area}
                    className="text-xs font-bold uppercase tracking-wide
                               text-[var(--rojo)] bg-[var(--rojo)]/10
                               px-3 py-1 rounded"
                  >
                    {area}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* ─── Palabras clave ─── */}
          <section className="mb-8">
            <h2 className="font-pixel text-xl text-[var(--rojo-oscuro)] mb-3">
              Palabras clave
            </h2>
            <div className="flex flex-wrap gap-2">
              {proyecto.palabrasClave.map((palabra) => (
                <span
                  key={palabra}
                  className="text-sm font-cuerpo
                             text-[var(--cafe)] bg-[var(--cafe)]/10
                             px-3 py-1 rounded-full"
                >
                  {palabra}
                </span>
              ))}
            </div>
          </section>

          {/* ─── Documentos ─── */}
          <section>
            <h2 className="font-pixel text-xl text-[var(--rojo-oscuro)] mb-3">
              Documentos
            </h2>

            <div className="flex items-center justify-between gap-4
                            bg-[var(--bg)] border border-[var(--cafe)]/20
                            rounded-lg p-4">
              <div className="flex flex-col">
                <strong className="font-cuerpo text-[var(--text-h)]">
                  Documento del proyecto
                </strong>
                <span className="text-xs text-[var(--cafe)]/70">
                  Archivo PDF
                </span>
              </div>

              <a
                href="#"
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 rounded-md bg-[var(--rojo)] text-[var(--bg)]
                           text-sm font-semibold hover:bg-[var(--azul)] transition"
              >
                Ver PDF
              </a>
            </div>
          </section>
        </article>

        {/* ═══════ SIDEBAR ═══════ */}
        <aside className="flex flex-col gap-4">
          
          {/* Información del proyecto */}
          <div className="bg-[var(--bg)] border border-[var(--cafe)]/20
                          rounded-lg p-5">
            <h3 className="font-pixel text-lg text-[var(--rojo-oscuro)] mb-4">
              Información del proyecto
            </h3>

            <div className="flex flex-col gap-3">
              <div className="flex flex-col">
                <span className="text-xs text-[var(--cafe)]/70">Departamento</span>
                <strong className="font-cuerpo text-[var(--text-h)]">
                  {proyecto.departamento}
                </strong>
              </div>

              <div className="flex flex-col">
                <span className="text-xs text-[var(--cafe)]/70">Estado</span>
                <strong className="font-cuerpo text-[var(--text-h)]">Publicado</strong>
              </div>

              <div className="flex flex-col">
                <span className="text-xs text-[var(--cafe)]/70">Año</span>
                <strong className="font-cuerpo text-[var(--text-h)]">
                  {new Date(proyecto.fecha).getFullYear()}
                </strong>
              </div>
            </div>
          </div>

          {/* Participantes */}
          <div className="bg-[var(--bg)] border border-[var(--cafe)]/20
                          rounded-lg p-5">
            <h3 className="font-pixel text-lg text-[var(--rojo-oscuro)] mb-4">
              Participantes
            </h3>

            <div className="flex flex-col gap-4">
              {/* Autor principal */}
              <div className="flex flex-col">
                <span className="font-cuerpo font-semibold text-[var(--text-h)]">
                  {proyecto.autor}
                </span>
                <span className="text-xs text-[var(--cafe)]/70">
                  Autor · Estudiante
                </span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
};

export default ProyectoDetalle;