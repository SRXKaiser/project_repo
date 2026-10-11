import { proyectosContent } from '../data/proyectosContent';
import type { FiltrosQuery, Proyecto, ResultadoProyectos } from '../types';

const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

export const proyectosService = {
  async buscar(params: FiltrosQuery = {}): Promise<ResultadoProyectos> {
    await delay(500);

    let filtrados = [...proyectosContent];

    if (params.query) {
      const q = params.query.toLowerCase();
      filtrados = filtrados.filter(
        (p) =>
          p.titulo.toLowerCase().includes(q) ||
          p.resumen.toLowerCase().includes(q) ||
          p.autor.toLowerCase().includes(q)
      );
    }

    if (params.titulo) {
      const q = params.titulo.toLowerCase();
      filtrados = filtrados.filter((p) => p.titulo.toLowerCase().includes(q));
    }
    if (params.autor) {
      const q = params.autor.toLowerCase();
      filtrados = filtrados.filter((p) => p.autor.toLowerCase().includes(q));
    }
    if (params.departamento) {
      filtrados = filtrados.filter((p) => p.departamento === params.departamento);
    }
    if (params.materia) {
      filtrados = filtrados.filter((p) => p.materia === params.materia);
    }
    if (params.palabrasClave?.length) {
      filtrados = filtrados.filter((p) =>
        params.palabrasClave!.some((pc) => p.palabrasClave.includes(pc))
      );
    }
    if (params.fechaDesde) {
      filtrados = filtrados.filter((p) => p.fecha >= params.fechaDesde!);
    }
    if (params.fechaHasta) {
      filtrados = filtrados.filter((p) => p.fecha <= params.fechaHasta!);
    }

    const orden = params.orden ?? 'recientes';
    if (orden === 'recientes') {
      filtrados.sort((a, b) => b.fecha.localeCompare(a.fecha));
    } else if (orden === 'populares') {
      filtrados.sort((a, b) => b.popularidad - a.popularidad);
    } else if (orden === 'alfabetico') {
      filtrados.sort((a, b) => a.titulo.localeCompare(b.titulo));
    }

    return { proyectos: filtrados, total: filtrados.length };
  },

  async populares(limit = 6): Promise<ResultadoProyectos> {
    await delay(400);
    const ordenados = [...proyectosContent].sort(
      (a, b) => b.popularidad - a.popularidad
    );
    return { proyectos: ordenados.slice(0, limit), total: proyectosContent.length };
  },

  async obtenerPorId(id: number): Promise<Proyecto | null> {
    await delay(300);
    return proyectosContent.find((p) => p.id === id) ?? null;
  },
};