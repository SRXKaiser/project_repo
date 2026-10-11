// ─── Opción de un dropdown ───
export interface Opcion {
  value: string;
  label: string;
}

// ═══════════════════════════════════════════════════════════
// TIPOS COMPARTIDOS DEL PROYECTO
// ═══════════════════════════════════════════════════════════

// ─── Proyecto ───
export interface Proyecto {
  id: number;
  titulo: string;
  autor: string;
  departamento: string;
  materia: string;
  palabrasClave: string[];
  fecha: string;           // ISO: "2025-08-15"
  resumen: string;
  popularidad: number;
  imagen: string | null;
}

// ─── Proyecto (ya lo tienes, agrega estado) ───
export type EstadoProyecto = 'Borrador' | 'En revisión' | 'Publicado' | 'Archivado';

export interface ProyectoDashboard {
  id: number;
  titulo: string;
  areaTematica: string;
  estado: EstadoProyecto;
  actualizadoEn: string;   // ISO date
}

// ─── Actividad ───
export interface Actividad {
  id: number;
  tipo: 'creado' | 'enviado' | 'publicado' | 'actualizado';
  titulo: string;          // "Proyecto enviado a revisión"
  descripcion: string;     // nombre del proyecto
  fecha: string;
}


// ─── Estadísticas ───
export interface EstadisticasDashboard {
  totalProyectos: number;
  borradores: number;
  enRevision: number;
  publicados: number;
}
// ─── Servicio (para CardService) ───
export interface Servicio {
  id: number;
  titulo: string;
  subtitulo: string;
  descripcion: string;
}

// ─── Razón de la caja azul (para BlueBox) ───
export interface RazonCaja {
  id: number;
  texto: string;
  align: 'left' | 'right';
}

// ─── Filtros ───
export interface Opcion {
  value: string;
  label: string;
}

export interface RangoFecha {
  desde: string;
  hasta: string;
}

export type TipoFiltro = 'text' | 'select' | 'multi' | 'date';

export type ValorFiltro = string | string[] | RangoFecha;

// ─── Estado interno del componente (TODO obligatorio) ───
export interface FiltrosProyecto {
  query: string;
  titulo: string;
  autor: string;
  departamento: string;
  materia: string;
  palabrasClave: string[];
  fecha: RangoFecha;
  orden: OrdenFiltro;
}

// ─── Valores por defecto ───
export const FILTROS_VACIOS: FiltrosProyecto = {
  query: '',
  titulo: '',
  autor: '',
  departamento: '',
  materia: '',
  palabrasClave: [],
  fecha: { desde: '', hasta: '' },
  orden: 'recientes',
};

export interface FiltrosQuery {
  query?: string;
  titulo?: string;
  autor?: string;
  departamento?: string;
  materia?: string;
  palabrasClave?: string[];
  fechaDesde?: string;
  fechaHasta?: string;
  orden?: OrdenFiltro;
}

// ─── Resultados de búsqueda ───
export interface ResultadoProyectos {
  proyectos: Proyecto[];
  total: number;
}

// ─── Usuario (para AuthContext) ───
export interface Usuario {
  id: number;
  name: string;
  email: string;
  role:  'estudiante' | 'docente' | 'admin';
}

// ─── Auth ───
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
  role: string;
}

export interface AuthResponse {
  user: Usuario;
  token: string;
}

export type OrdenFiltro = 'recientes' | 'populares' | 'alfabetico';



