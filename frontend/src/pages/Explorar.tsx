import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import FondoCategorias from '../components/FondoCategorias';
import FiltrosBar from '../components/FiltrosBar';
import Banner from '../components/Banner';
import ModalRegistro from '../components/ModalRegistro';
import CardProyecto from '../components/CardProyecto';
import { useProyectos } from '../hooks/useProyectos';
import { useAuth } from '../context/AuthContext';
import { FILTROS_VACIOS } from '../types';
import type { FiltrosProyecto, Proyecto } from '../types';

const Explorar = () => {
  const { user } = useAuth();
  const [filtros, setFiltros] = useState<FiltrosProyecto>(FILTROS_VACIOS);
  const [activado, setActivado] = useState(false);
  const [proyectoSeleccionado, setProyectoSeleccionado] = useState<Proyecto | null>(null);

  const {
    proyectos,
    total,
    loading,
    hayBusqueda,
    buscar,
    resetear,
  } = useProyectos();

  // ─── Búsqueda desde el SearchBar (solo texto) ───
  const handleSearch = (query: string) => {
    setActivado(true);
    const nuevos: FiltrosProyecto = { ...filtros, query };
    setFiltros(nuevos);
    buscar(nuevos);
  };

  // ─── Cambio en FiltrosBar ───
  const handleFiltrosChange = (nuevosFiltros: FiltrosProyecto) => {
    setFiltros(nuevosFiltros);
    setActivado(true);
    buscar(nuevosFiltros);
  };

  const handleActivar = () => setActivado(true);

  const handleProyectoClick = (proyecto: Proyecto) => {
    setProyectoSeleccionado(proyecto);
  };

  return (
    <div
      className={`
        relative min-h-screen transition-colors duration-300
        ${activado
          ? 'bg-[var(--bg)]'
          : 'bg-[radial-gradient(circle_at_bottom,_var(--rojo-oscuro)_10%,_var(--rey)_100%)]'
        }
      `}
    >
      {!activado && <FondoCategorias cantidad={45} />}

      {/* ─── STICKY: barra + filtros ─── */}
      <div
        className={`
          sticky top-16 z-30 transition-all duration-300
          ${activado
            ? 'bg-[var(--bg)] shadow-md border-b border-[var(--cafe)]/20 py-3 translate-y-0'
            : 'bg-transparent py-16 -translate-y-8'
          }
        `}
      >
        <div className="max-w-7xl mx-auto px-6">
          {!activado && (
            <div className="text-center mb-3 max-w-3xl mx-auto">
              <h1 className="text-3xl font-bold text-[var(--bg)] mb-1">
                EXPLORA EL CONOCIMIENTO DE NUESTRA COMUNIDAD
              </h1>
              <p className="font-cuerpo text-lg text-[var(--bg)]">
                Busca por título, autor, palabra clave o filtra por categoría.
              </p>
            </div>
          )}

          {!activado && (
            <div
              className="flex flex-col items-center gap-3"
              onFocus={handleActivar}
              onClick={handleActivar}
            >
              <div className="w-full max-w-2xl">
                <SearchBar value={filtros.query} onSearch={handleSearch} />
              </div>
              <div className="justify-center">
                <FiltrosBar filtros={filtros} onChange={handleFiltrosChange} />
              </div>
            </div>
          )}

          {activado && (
            <div
              className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3"
              onClick={handleActivar}
            >
              <div className="flex-1 min-w-0">
                <SearchBar value={filtros.query} onSearch={handleSearch} />
              </div>
              <div className="shrink-0">
                <FiltrosBar filtros={filtros} onChange={handleFiltrosChange} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ─── RESULTADOS ─── */}
      {activado && (
        <div className="relative z-10 px-6 pb-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex items-baseline justify-between mb-6 mt-6">
              <h2 className="font-pixel text-2xl text-[var(--rojo-oscuro)]">
                {hayBusqueda ? 'Resultados de búsqueda' : 'Proyectos populares'}
              </h2>
              {!loading && (
                <span className="font-cuerpo text-sm text-[var(--cafe)]/70">
                  {total} proyecto{total !== 1 ? 's' : ''}
                </span>
              )}
            </div>

            {loading && (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className="animate-pulse bg-[var(--cafe)]/10 rounded-lg h-80"
                  />
                ))}
              </div>
            )}

            {!loading && proyectos.length === 0 && (
              <div className="text-center py-16">
                <p className="font-pixel text-2xl text-[var(--cafe)]/70 mb-2">
                  No se encontraron proyectos
                </p>
                <p className="font-cuerpo text-[var(--cafe)]/60 mb-4">
                  Prueba con otros filtros o términos de búsqueda.
                </p>
                <button
                  onClick={resetear}
                  className="px-6 py-2 rounded-md bg-[var(--rojo)] text-[var(--bg)]
                             font-semibold hover:bg-[var(--azul)] transition"
                >
                  Ver populares
                </button>
              </div>
            )}

            {!loading && proyectos.length > 0 && (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {proyectos.map((p) => (
                  <CardProyecto
                    key={p.id}
                    proyecto={p}
                    onClick={handleProyectoClick}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {!user && <Banner />}

      {proyectoSeleccionado && (
        <ModalRegistro
          proyecto={proyectoSeleccionado}
          onClose={() => setProyectoSeleccionado(null)}
        />
      )}
    </div>
  );
};

export default Explorar;