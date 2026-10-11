import type { Opcion} from '../types';

// ─── Opciones (temporal, después vendrán de la BD) ───
export const DEPARTAMENTOS = [
  { value: 'sistemas', label: 'Sistemas y Computación' },
  { value: 'industrial', label: 'Ingeniería Industrial' },
  { value: 'electrica', label: 'Ingeniería Eléctrica' },
  { value: 'mecanica', label: 'Ingeniería Mecánica' },
  { value: 'civil', label: 'Ingeniería Civil' },
  { value: 'gestion', label: 'Gestión Empresarial' },
  { value: 'ciencias', label: 'Ciencias Básicas' },
];

export const MATERIAS_POR_DEPARTAMENTO: Record<string, Opcion[]> = {
  sistemas: [
    { value: 'programacion', label: 'Programación' },
    { value: 'bases-datos', label: 'Bases de Datos' },
    { value: 'redes', label: 'Redes' },
    { value: 'ia', label: 'Inteligencia Artificial' },
    { value: 'web', label: 'Desarrollo Web' },
  ],
  industrial: [
    { value: 'logistica', label: 'Logística' },
    { value: 'calidad', label: 'Control de Calidad' },
    { value: 'produccion', label: 'Producción' },
    { value: 'seguridad', label: 'Seguridad Industrial' },
  ],
  electrica: [
    { value: 'circuitos', label: 'Circuitos Eléctricos' },
    { value: 'potencia', label: 'Sistemas de Potencia' },
    { value: 'control', label: 'Control Automático' },
  ],
  mecanica: [
    { value: 'termodinamica', label: 'Termodinámica' },
    { value: 'materiales', label: 'Ciencia de Materiales' },
    { value: 'diseno', label: 'Diseño Mecánico' },
  ],
  civil: [
    { value: 'estructuras', label: 'Estructuras' },
    { value: 'hidraulica', label: 'Hidráulica' },
    { value: 'geotecnia', label: 'Geotecnia' },
  ],
  gestion: [
    { value: 'marketing', label: 'Marketing' },
    { value: 'finanzas', label: 'Finanzas' },
    { value: 'rrhh', label: 'Recursos Humanos' },
  ],
  ciencias: [
    { value: 'fisica', label: 'Física' },
    { value: 'quimica', label: 'Química' },
    { value: 'matematicas', label: 'Matemáticas' },
  ],
};

export const PALABRAS_CLAVE = [
  { value: 'ia', label: 'Inteligencia Artificial' },
  { value: 'iot', label: 'IoT' },
  { value: 'automatizacion', label: 'Automatización' },
  { value: 'sustentabilidad', label: 'Sustentabilidad' },
  { value: 'robotica', label: 'Robótica' },
  { value: 'bigdata', label: 'Big Data' },
  { value: 'blockchain', label: 'Blockchain' },
  { value: 'energias', label: 'Energías Renovables' },
];

export const categoriasDefault = [
  'Ingeniería',
  'Ciencias',
  'Ciencias Sociales',
  'Tecnología',
  'Matemáticas',
  'Física',
  'Química',
  'Biología',
  'Medicina',
  'Arquitectura',
  'Economía',
  'Psicología',
  'Educación',
  'Derecho',
  'Humanidades',
  'Arte',
  'Historia',
  'Filosofía',
  'Computación',
  'Electrónica',
  'Mecánica',
  'Industrial',
  'Ambiental',
  'Energía',
];

