import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import type { Proyecto } from '../types';

interface ModalRegistroProps {
  proyecto: Proyecto | null;
  onClose: () => void;
}

const ModalRegistro = ({ proyecto, onClose }: ModalRegistroProps) => {
  // Cerrar con Escape
useEffect(() => {
  const prevOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';

  const handleEsc = (e: KeyboardEvent) => {
    if (e.key === 'Escape') onClose();
  };
  document.addEventListener('keydown', handleEsc);

  return () => {
    document.body.style.overflow = prevOverflow;   // ← restaurar
    document.removeEventListener('keydown', handleEsc);
  };
}, [onClose]);
  if (!proyecto) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Card */}
      <div className="relative bg-[var(--bg)] rounded-2xl shadow-2xl
                      w-full max-w-2xl max-h-[90vh] overflow-y-auto
                      animate-modal-in">

        {/* Botón cerrar */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 z-10 p-2 rounded-full
                     bg-[var(--bg)] hover:bg-[var(--rojo)]/10
                     text-[var(--cafe)] transition"
          aria-label="Cerrar"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18 18 6M6 6l12 12" />
          </svg>
        </button>

        {/* Imagen/header */}
        <div className="h-48 bg-[var(--rojo-oscuro)]/10 flex items-center justify-center">
          {proyecto.imagen ? (
            <img src={proyecto.imagen} alt="proyecto.titulo" className="w-full h-full object-cover" />
          ) : (
            <span className="font-pixel text-5xl text-[var(--rojo-oscuro)]/30">📄</span>
          )}
        </div>

        {/* Contenido */}
        <div className="p-6 md:p-8">
          <span className="inline-block text-xs font-bold uppercase tracking-wide
                           text-[var(--rojo)] bg-[var(--rojo)]/10
                           px-2 py-1 rounded mb-3">
            {proyecto.departamento}
          </span>

          <h2 className="font-pixel text-2xl text-[var(--rojo-oscuro)] mb-3">
            {proyecto.titulo}
          </h2>

          <div className="flex flex-wrap gap-4 text-sm text-[var(--cafe)]/80 mb-4">
            <span>👤 {proyecto.autor}</span>
            <span>
              📅{' '}
              {new Date(proyecto.fecha).toLocaleDateString('es-MX', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </span>
            <span>❤️ {proyecto.popularidad}</span>
          </div>

          <p className="font-cuerpo text-[var(--cafe)] leading-relaxed mb-6">
            {proyecto.resumen}
          </p>

          {/* CTA */}
          <div className="bg-gradient-to-br from-[var(--rojo)]/5 to-[var(--azul)]/5
                          border border-[var(--rojo)]/20
                          rounded-xl p-6 text-center">
            <h3 className="font-pixel text-xl text-[var(--rojo-oscuro)] mb-2">
              🔒 Acceso restringido
            </h3>
            <p className="font-cuerpo text-sm text-[var(--cafe)] mb-5 max-w-md mx-auto">
              Para ver el contenido completo de este proyecto, sus archivos y
              contactar al autor, necesitas una cuenta.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link
                to="/register"
                className="px-6 py-2.5 rounded-md bg-[var(--rojo)] text-[var(--bg)]
                           font-semibold hover:bg-[var(--azul)] transition"
              >
                Crear cuenta gratis
              </Link>
              <Link
                to="/login"
                className="px-6 py-2.5 rounded-md border border-[var(--cafe)]/30
                           text-[var(--cafe)] font-semibold
                           hover:bg-[var(--rojo)]/10 transition"
              >
                Iniciar sesión
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModalRegistro;