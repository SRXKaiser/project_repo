import { useState, useRef, useEffect } from 'react';
import type { Opcion, RangoFecha, TipoFiltro, ValorFiltro } from '../types';

//props
interface FilterDropProps {
  label: string;
  tipo?: TipoFiltro;
  opciones?: Opcion[];
  valor?: ValorFiltro;
  onChange: (valor: ValorFiltro) => void;
  placeholder?: string;
  disabled?: boolean;
  disabledHint?: string;
}


const FilterDrop = ({
  label,
  tipo = 'select',
  opciones = [],
  valor = '',
  onChange,
  placeholder = 'Buscar...',
  disabled = false,                          
  disabledHint = 'No disponible',     
}: FilterDropProps) => {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Cerrar al hacer clic fuera
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

   // Bloquear apertura si está deshabilitado
  const handleToggle = () => {
    if (disabled) return;
    setOpen((o) => !o);
  };

  // Helpers de tipo 
  const esRangoFecha = (v: ValorFiltro): v is RangoFecha =>
    typeof v === 'object' && !Array.isArray(v);

  const esArray = (v: ValorFiltro): v is string[] => Array.isArray(v);

  const esString = (v: ValorFiltro): v is string => typeof v === 'string';

  // Determinar si hay valor activo (para mostrar en el botón)
    const tieneValor = (() => {
    if (tipo === 'date' && esRangoFecha(valor)) {
      return Boolean(valor?.desde || valor?.hasta);
    }
    if (Array.isArray(valor)) return valor.length > 0;
    return Boolean(valor);
  })();

  // Texto a mostrar en el botón
  const textoMostrado = (() => {
  // Fecha: manejo especial
   if (tipo === 'date' && esRangoFecha(valor)) {
      const { desde, hasta } = valor;
      if (!desde && !hasta) return label;
      if (desde && hasta) return `${desde} → ${hasta}`;
      if (desde) return `Desde ${desde}`;
      return `Hasta ${hasta}`;
    }

  // Array (multi)
  if (Array.isArray(valor)) {
    if (valor.length === 0) return label;
    if (valor.length === 1) {
      return opciones.find((o) => o.value === valor[0])?.label || valor[0];
    }
    return `${label} (${valor.length})`;
  }

  // Sin valor
  if (!valor) return label;

  // Select / multi
  if (tipo === 'select' && esString(valor)) {
      return opciones.find((o) => o.value === valor)?.label || valor;
    }

    // Text
    if (esString(valor)) return valor;

    return label;
  })();

  // ─── Render según tipo ───
  const renderContenido = () => {
    // TEXTO (título, autor)
    if (tipo === 'text') {
      return (
        <input
          type="text"
          value={esString(valor) ? valor : ''}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          autoFocus
          className="w-full px-3 py-2 rounded-md border border-[var(--cafe)]/30
                     bg-[var(--bg)] text-[var(--text-h)] text-sm
                     focus:outline-none focus:ring-2 focus:ring-[var(--rojo)]/30"
        />
      );
    }

    // FECHA
    if (tipo === 'date') {
      const rango: RangoFecha = esRangoFecha(valor)
        ? valor
        : { desde: '', hasta: '' };
      return (
        <div className="space-y-2">
          <label className="text-xs text-[var(--cafe)]">Desde</label>
          <input
            type="date"
            value={rango.desde}
            onChange={(e) => onChange({ ...rango, desde: e.target.value })}
            className="w-full px-3 py-2 rounded-md border border-[var(--cafe)]/30
                       bg-[var(--bg)] text-[var(--text-h)] text-sm
                       focus:outline-none focus:ring-2 focus:ring-[var(--rojo)]/30"
          />
          <label className="text-xs text-[var(--cafe)]">Hasta</label>
          <input
            type="date"
            value={rango.hasta}
            onChange={(e) => onChange({ ...rango, hasta: e.target.value })}
            className="w-full px-3 py-2 rounded-md border border-[var(--cafe)]/30
                       bg-[var(--bg)] text-[var(--text-h)] text-sm
                       focus:outline-none focus:ring-2 focus:ring-[var(--rojo)]/30"
          />
        </div>
      );
    }

// ─── SELECT ───
    if (tipo === 'select') {
      const valorStr = esString(valor) ? valor : '';

      return (
        <ul className="max-h-60 overflow-y-auto">
          <li>
            <button
              type="button"
              onClick={() => {
                onChange('');
                setOpen(false);
              }}
              className={`w-full text-left px-3 py-2 rounded-md text-sm
                          ${!valorStr
                            ? 'bg-[var(--rojo)]/10 text-[var(--rojo)]'
                            : 'text-[var(--cafe)] hover:bg-[var(--rojo)]/10'
                          }`}
            >
              Todas
            </button>
          </li>
          {opciones.map((op) => (
            <li key={op.value}>
              <button
                type="button"
                onClick={() => {
                  onChange(op.value);
                  setOpen(false);
                }}
                className={`w-full text-left px-3 py-2 rounded-md text-sm
                            ${valorStr === op.value
                              ? 'bg-[var(--rojo)]/10 text-[var(--rojo)]'
                              : 'text-[var(--cafe)] hover:bg-[var(--rojo)]/10'
                            }`}
              >
                {op.label}
              </button>
            </li>
          ))}
        </ul>
      );
    }

    // ─── MULTI ───
    if (tipo === 'multi') {
      const valores: string[] = esArray(valor) ? valor : [];

      const toggle = (v: string) => {
        const nuevos = valores.includes(v)
          ? valores.filter((x) => x !== v)
          : [...valores, v];
        onChange(nuevos);
      };

      return (
        <ul className="max-h-60 overflow-y-auto">
          {opciones.map((op) => {
            const activo = valores.includes(op.value);
            return (
              <li key={op.value}>
                <button
                  type="button"
                  onClick={() => toggle(op.value)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm
                              ${activo
                                ? 'bg-[var(--rojo)]/10 text-[var(--rojo)]'
                                : 'text-[var(--cafe)] hover:bg-[var(--rojo)]/10'
                              }`}
                >
                  <span
                    className={`w-4 h-4 rounded border flex items-center justify-center
                                ${activo
                                  ? 'bg-[var(--rojo)] border-[var(--rojo)]'
                                  : 'border-[var(--cafe)]/40'
                                }`}
                  >
                    {activo && (
                      <svg
                        className="w-3 h-3 text-white"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path d="M16.7 5.3a1 1 0 0 1 0 1.4l-7 7a1 1 0 0 1-1.4 0l-3-3a1 1 0 1 1 1.4-1.4L9 11.6l6.3-6.3a1 1 0 0 1 1.4 0z" />
                      </svg>
                    )}
                  </span>
                  {op.label}
                </button>
              </li>
            );
          })}
        </ul>
      );
    }

    return null;
  };

  // ─── Limpiar ───
  const handleLimpiar = () => {
    if (esArray(valor)) {
      onChange([]);
    } else if (tipo === 'date') {
      onChange({ desde: '', hasta: '' });
    } else {
      onChange('');
    }
    setOpen(false);
  };

  return (
    <div className="relative" ref={ref}>
      {/* Botón */}
      <button
        type="button"
        onClick={handleToggle}
        disabled={disabled}
        title={disabled ? disabledHint : ''}
        className={`
          inline-flex items-center gap-2 px-4 py-2.5 rounded-lg
          text-sm font-medium whitespace-nowrap
          transition-colors duration-150
          ${disabled
            ? 'bg-[var(--cafe)]/10 text-[var(--cafe)]/40 border border-[var(--cafe)]/20 cursor-not-allowed'
            : tieneValor
              ? 'bg-[var(--rojo)]/15 text-[var(--rojo)] border border-[var(--rojo)]/40'
              : 'bg-[var(--bg)] text-[var(--cafe)] border border-[var(--cafe)]/30 hover:bg-[var(--rojo)]/5'
          }
        `}
      >
        {disabled ? `${label} 🔒` : textoMostrado}
        <svg
          className={`w-4 h-4 transition-transform duration-200 ${open ? 'rotate-180' : ''}`}
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke="currentColor"
            strokeLinecap="round"
            strokeWidth="2"
            d="m19 9-7 7-7-7"
          />
        </svg>
      </button>

      {/* Panel */}
      {open && !disabled && (
        <div
          className="absolute top-full left-0 mt-2 z-30 min-w-[220px] max-w-xs
                     bg-[var(--bg)] border border-[var(--cafe)]/20
                     rounded-lg shadow-xl p-2"
        >
          {renderContenido()}

          {tieneValor && (
            <button
              type="button"
              onClick={handleLimpiar}
              className="w-full text-xs text-[var(--cafe)]/70 hover:text-[var(--rojo)]
                         mt-2 pt-2 border-t border-[var(--cafe)]/20 transition text-center"
            >
              Limpiar
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default FilterDrop;