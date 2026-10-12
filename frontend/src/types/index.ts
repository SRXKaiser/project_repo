
// ═══════════════════════════════════════════════════════════
// TIPOS COMPARTIDOS DEL PROYECTO
// ═══════════════════════════════════════════════════════════

// Proyecto
export interface Proyecto {
  id: number;
  titulo: string;
  autor: string;
  departamento: string;
  materia: string;
  palabrasClave: string[];
  fecha: string; //estandar: "2025-08-15"
  resumen: string;
  popularidad: number;
  imagen: string | null;
}

//Proyecto
export type EstadoProyecto = 'Borrador' | 'En revisión' | 'Publicado' | 'Archivado';

export interface ProyectoDashboard {
  id: number;
  titulo: string;
  areaTematica: string;
  estado: EstadoProyecto;
  actualizadoEn: string;//date
}

// Actividad
export interface Actividad {
  id: number;
  tipo: 'creado' | 'enviado' | 'publicado' | 'actualizado';
  titulo: string;          // "Proyecto enviado a revisión"
  descripcion: string;     // nombre del proyecto
  fecha: string;
}


// Estadísticas
export interface EstadisticasDashboard {
  totalProyectos: number;
  borradores: number;
  enRevision: number;
  publicados: number;
}
// Servicio (para CardService)
export interface Servicio {
  id: number;
  titulo: string;
  subtitulo: string;
  descripcion: string;
}

// Razón de la caja azul (para BlueBox)
export interface RazonCaja {
  id: number;
  texto: string;
  align: 'left' | 'right';
}

// Filtros de busqueda
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

// Estado interno del componente (TODO obligatorio)
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

// Valores por defecto
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

// Resultados de búsqueda
export interface ResultadoProyectos {
  proyectos: Proyecto[];
  total: number;
}

// Usuario (para AuthContext) 
export interface Usuario {
  id: number;
  name: string;
  email: string;
  role:  'ESTUDIANTE' | 'DOCENTE' | 'EGRESADO';
}

//
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


//------------------PARA BASE DE DATOS

export type TipoUsuario = 'ESTUDIANTE' | 'DOCENTE' | 'EGRESADO';

//1. END POINT REGISTER
export interface RegistroPayload {
  nombre: string;
  apellido_paterno: string;
  apellido_materno: string;
  correo: string;
  password: string;
  tipo_usuario: TipoUsuario;
// Datos para quien seleccione estudiante
  num_control?: string;
  id_carrera?: number;
  semestre?: number;
  // empleado
  num_empleado?: string;
  id_departamento?: number;
  //exalumno
  anio_egreso?: number;
}


export interface RegistroResponse {
  id: number;
  nombre: string;
  correo: string;
  tipo_usuario: TipoUsuario;
  mensaje?: string;
}

export interface ApiError {
  detail?: string | { msg: string; loc: string[] }[];
}

//2. ENDPOINT DE DEPARTAMENTOS, PARA FILTRAR LA LISTA
export interface Departamentos {
  id_departamento: number;
  nombre: string;
  descripcion: string | null;
}

//3. LO MISMO PERO AHORA PARA LAS CARRERAS SI EL USUARIO ES ALUMNO
export interface Carreras {
   id_carrera: number;
   nombre: string;
   siglas: string;
   //activa?: boolean;
   id_departamento: number;
}

//-----------ESTO ES PARA EL MOMENTO EN QUE EL USUARIO HAGA LOGIN
export type EstadoCuenta = 'ACTIVA' | 'INACTIVA' | 'SUSPENDIDA';

export interface Usuario {
  id_usuario: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno: string;
  correo: string;
  tipo_usuario: TipoUsuario;
  estado_cuenta: EstadoCuenta;
  fecha_registro: string;         // ISO
  ultimo_acceso: string;          // ISO
  es_administrador: boolean;
  departamentos_responsable: number[];
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
