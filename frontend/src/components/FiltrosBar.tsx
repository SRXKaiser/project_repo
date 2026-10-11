import FilterDrop from './FilterDrop';
import {
  DEPARTAMENTOS,
  MATERIAS_POR_DEPARTAMENTO,
  PALABRAS_CLAVE,
} from '../data/explorarContent';
import type { FiltrosProyecto, ValorFiltro } from '../types';
import { FILTROS_VACIOS } from '../types';

interface FiltrosBarProps {
  filtros: FiltrosProyecto;                          // ← controlado
  onChange?: (filtros: FiltrosProyecto) => void;
}

const FiltrosBar = ({ filtros, onChange }: FiltrosBarProps) => {
  const materiasDisponibles = filtros.departamento
    ? MATERIAS_POR_DEPARTAMENTO[filtros.departamento] ?? []
    : [];

  const setFiltro = <K extends keyof FiltrosProyecto>(
    key: K,
    value: FiltrosProyecto[K]
  ) => {
    const nuevos: FiltrosProyecto = { ...filtros, [key]: value };

    // Si cambia el departamento → resetear materia
    if (key === 'departamento' && value !== filtros.departamento) {
      nuevos.materia = '';
    }

    onChange?.(nuevos);
  };

  const filtrosActivos = [
    filtros.titulo,
    filtros.departamento,
    filtros.materia,
    filtros.fecha.desde || filtros.fecha.hasta,
    filtros.autor,
    filtros.palabrasClave.length > 0,
  ].filter(Boolean).length;

  return (
    <div className="w-full">
      {filtrosActivos > 0 && (
        <div className="flex items-center justify-between mb-0">
          <span className="text-sm text-[var(--cafe)]">
            <strong className="text-[var(--rojo)]">{filtrosActivos}</strong>{' '}
            filtro{filtrosActivos > 1 ? 's' : ''} activo
            {filtrosActivos > 1 ? 's' : ''}
          </span>
          <button
            type="button"
            onClick={() => onChange?.({ ...filtros, ...FILTROS_VACIOS, query: filtros.query })}
            className="text-xs text-[var(--cafe)]/70 hover:text-[var(--rojo)] transition"
          >
            Limpiar todos
          </button>
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        <FilterDrop
          label="Departamento"
          tipo="select"
          opciones={DEPARTAMENTOS}
          valor={filtros.departamento}
          onChange={(v) => setFiltro('departamento', v as string)}
        />

        <FilterDrop
          label="Materia"
          tipo="select"
          opciones={materiasDisponibles}
          valor={filtros.materia}
          onChange={(v) => setFiltro('materia', v as string)}
          disabled={!filtros.departamento}
          disabledHint="Selecciona un departamento primero"
        />

        <FilterDrop
          label="Fecha de creación"
          tipo="date"
          valor={filtros.fecha}
          onChange={(v) => setFiltro('fecha', v as any)}
        />

        <FilterDrop
          label="Autor"
          tipo="text"
          valor={filtros.autor}
          onChange={(v) => setFiltro('autor', v as string)}
          placeholder="Nombre del autor..."
        />

        <FilterDrop
          label="Palabras clave"
          tipo="multi"
          opciones={PALABRAS_CLAVE}
          valor={filtros.palabrasClave}
          onChange={(v) => setFiltro('palabrasClave', v as string[])}
        />
      </div>
    </div>
  );
};

export default FiltrosBar;