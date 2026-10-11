import { useState, useEffect, useCallback } from 'react';
import { proyectosService } from '../services/proyectoService';
import { filtrosAQuery } from '../utils/filtros';
import type { FiltrosProyecto, Proyecto, ResultadoProyectos } from '../types';

export const useProyectos = () => {
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [hayBusqueda, setHayBusqueda] = useState(false);

  useEffect(() => {
    let cancelado = false;
    const cargar = async () => {
      setLoading(true);
      try {
        const { proyectos, total } = await proyectosService.populares(6);
        if (!cancelado) {
          setProyectos(proyectos);
          setTotal(total);
        }
      } catch (err) {
        if (!cancelado) setError(err as Error);
      } finally {
        if (!cancelado) setLoading(false);
      }
    };
    cargar();
    return () => { cancelado = true; };
  }, []);

  const buscar = useCallback(async (filtros: FiltrosProyecto) => {
    setLoading(true);
    setError(null);
    setHayBusqueda(true);
    try {
      // ⭐ Convertir filtros a query params
      const query = filtrosAQuery(filtros);
      const { proyectos, total } = await proyectosService.buscar(query);
      setProyectos(proyectos);
      setTotal(total);
    } catch (err) {
      setError(err as Error);
      setProyectos([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, []);

  const resetear = useCallback(async () => {
    setLoading(true);
    try {
      const { proyectos, total } = await proyectosService.populares(6);
      setProyectos(proyectos);
      setTotal(total);
      setHayBusqueda(false);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  }, []);

  return { proyectos, total, loading, error, buscar, resetear, hayBusqueda };
};