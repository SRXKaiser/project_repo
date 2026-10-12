import axios from 'axios';
import api from './api';
import type { RegistroPayload, RegistroResponse, LoginResponse, Usuario, ApiError } from '../types';

//PARA INTERPRETAR LOS MENSAJES de tipo ya existe el correo, error de conexxion, etc

const extraerMensajeError = (error: unknown): string => {
  if (!axios.isAxiosError(error)) {
    return 'Error desconocido';
  }

  // No hubo respuesta (servidor caído, red, CORS, etc.)
  if (!error.response) {
    return 'No se pudo conectar con el servidor. Verifica tu conexión.';
  }

  const detail = error.response.data?.detail;

  // detail es un string → error de negocio
  if (typeof detail === 'string') {
    return detail;
  }

  // detail es un array → error de validación de Pydantic
  if (Array.isArray(detail) && detail.length > 0) {
    const primero = detail[0];
    const campo = primero.loc?.slice(-1)[0] ?? 'campo';
    return `${campo}: ${primero.msg}`;
  }

  // Fallback
  return error.response.data?.message ?? `Error ${error.response.status}`;
};

export const authService = {
  
// REGISTEO DE USUARIO
// POST/auth/register
  async registrarUsuario(payload: RegistroPayload): Promise<RegistroResponse> {
    try {
      const { data } = await api.post<RegistroResponse>('/auth/register', payload);
      return data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail;
        if (typeof detail === 'string') throw new Error(detail);
        if (Array.isArray(detail)) {
          throw new Error(detail.map((d: any) => d.msg).join(', '));
        }
        throw new Error(`Error ${error.response?.status}: ${error.message}`);
      }
      throw error;
    }
  },
  
  /**
   * Login completo YA AHORA SI DE VERDAD ES EL ULTIMO
   * 1. POST /auth/login obtener el token
   * 2. GET /auth/me  usuario usuario
   * 3. Guardar ambos en localStorage
   * 4. Devolver el usuario
   */
  async login(correo: string, password: string): Promise<Usuario> {
    try {
      // toke
      const { data: loginData } = await api.post<LoginResponse>('/auth/login', {
        correo,
        password,
      });

      // guardar token temporalmente 
      localStorage.setItem('token', loginData.access_token);

      //obtener usuario con el token
      const { data: usuario } = await api.get<Usuario>('/usuarios/me');

      //guardar el usuario
      localStorage.setItem('user', JSON.stringify(usuario));

      return usuario;
    } catch (err) {
      // limpiar si algo falla
      localStorage.removeItem('token');
      localStorage.removeItem('user');

      if (axios.isAxiosError(err)) {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') throw new Error(detail);
        if (Array.isArray(detail)) {
          throw new Error(detail.map((d: any) => d.msg).join(', '));
        }
        throw new Error(`Error ${err.response?.status}: ${err.message}`);
      }
      throw err;
    }
  },
};