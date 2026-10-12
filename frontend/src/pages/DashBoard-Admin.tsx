import { useAuth } from '../context/AuthContext';
import DashboardLayout from '../components/user-dashboard/DBLayout';
import DashboardWelcome from '../components/user-dashboard/DBWelcome';
import DashboardStats from '../components/user-dashboard/DBStats';
import DashboardProjects from '../components/user-dashboard/DSProject';
import DashboardActivity from '../components/user-dashboard/DBActivity';
import type {
  ProyectoDashboard,
  Actividad,
  EstadisticasDashboard,
} from '../types';

//Datos mock para mostrar las tarjetas en lo que hay infomracin real en la db
const PROYECTOS_MOCK: ProyectoDashboard[] = [
  {
    id: 1,
    titulo: 'Sistema inteligente para análisis de información académica',
    areaTematica: 'Inteligencia Artificial',
    estado: 'En revisión',
    actualizadoEn: '2026-10-01',
  },
  {
    id: 2,
    titulo: 'Plataforma de gestión universitaria',
    areaTematica: 'Desarrollo de Software',
    estado: 'Publicado',
    actualizadoEn: '2026-09-20',
  },
  {
    id: 3,
    titulo: 'Análisis de datos académicos',
    areaTematica: 'Bases de Datos',
    estado: 'Borrador',
    actualizadoEn: '2026-09-15',
  },
];

const ACTIVIDADES_MOCK: Actividad[] = [
  {
    id: 1,
    tipo: 'enviado',
    titulo: 'Proyecto enviado a revisión',
    descripcion: 'Sistema inteligente para análisis...',
    fecha: '2026-10-01',
  },
  {
    id: 2,
    tipo: 'publicado',
    titulo: 'Proyecto publicado',
    descripcion: 'Plataforma de gestión universitaria',
    fecha: '2026-09-20',
  },
  {
    id: 3,
    tipo: 'creado',
    titulo: 'Proyecto creado',
    descripcion: 'Análisis de datos académicos',
    fecha: '2026-09-15',
  },
];

const DashboardAdmin = () => {
  const { user } = useAuth();

  if (!user) return null;

  // Estadísticas calculadas de los proyectos
  const stats: EstadisticasDashboard = {
    totalProyectos: PROYECTOS_MOCK.length,
    borradores: PROYECTOS_MOCK.filter((p) => p.estado === 'Borrador').length,
    enRevision: PROYECTOS_MOCK.filter((p) => p.estado === 'En revisión').length,
    publicados: PROYECTOS_MOCK.filter((p) => p.estado === 'Publicado').length,
  };

  // Primer nombre para la bienvenida
  const primerNombre = user.nombre.split(' ')[0];

  return (
    <>
      <DashboardWelcome nombre={primerNombre} mensaje={'ESTE ES EL DASHBOARD DEL ADMIN'} />
      <DashboardStats stats={stats} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <img src="../src/assets/enConstruccion.jpg" alt="" />
        </div>
        <DashboardActivity actividades={ACTIVIDADES_MOCK} />
      </div>
    </>
  );
};

export default DashboardAdmin;