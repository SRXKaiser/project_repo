import type { FiltrosProyecto, FiltrosQuery } from '../types';

/**
 * Convierte el estado completo de filtros a un objeto
 * con solo los campos que tienen valor. Útil para mandar
 * al backend como query params.
 * 
 * Cómo funciona: itera los campos. Si tienen valor, los agrega. Si están vacíos, los omite. Así al backend solo van los filtros activos.


 */
export const filtrosAQuery = (filtros: FiltrosProyecto): FiltrosQuery => {
  const query: FiltrosQuery = {};

  if (filtros.query.trim()) query.query = filtros.query.trim();
  if (filtros.titulo.trim()) query.titulo = filtros.titulo.trim();
  if (filtros.autor.trim()) query.autor = filtros.autor.trim();
  if (filtros.departamento) query.departamento = filtros.departamento;
  if (filtros.materia) query.materia = filtros.materia;
  if (filtros.palabrasClave.length > 0) query.palabrasClave = filtros.palabrasClave;
  if (filtros.fecha.desde) query.fechaDesde = filtros.fecha.desde;
  if (filtros.fecha.hasta) query.fechaHasta = filtros.fecha.hasta;
  if (filtros.orden !== 'recientes') query.orden = filtros.orden;

  return query;
};