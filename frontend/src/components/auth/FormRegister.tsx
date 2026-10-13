import { useState, useEffect } from 'react';
import type { FormEvent } from 'react';
import AuthLayout from './AuthLayout';
import AuthHeader from './AuthHeader';
import Input from '../Input';
import AuthFooter from './AuthFooter';
import IndicadorPasos from './IndicadorPasos';
import TipoUsuarioRadio from './TipoUserRadio';
import BtnNavegar from './BtnNavegar';
import AnimacionParte from './AnimacionParte';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';
import { departamentosService } from '../../services/departamentoService';
import { carrerasService } from '../../services/carreraService';
import type { RegistroPayload } from '../../types';
import type { Departamentos } from '../../types';
import type { Carreras } from '../../types';



type Tipo_Usuario = 'ESTUDIANTE' | 'DOCENTE' | 'EGRESADO' | '';

const FormRegister = () => {
  const [paso, setPaso] = useState<1 | 2 | 3 | 4>(1);
  const [direccion, setDireccion] = useState<'adelante' | 'atras'>('adelante');
  const navigate = useNavigate();

  // 1. datos digitales
  const [correo, setcorreo] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  //2. nombre
  const [nombre, setNombre] = useState('');
  const [apellido_paterno, setapellido_paterno] = useState('');
  const [apellido_materno, setapellido_materno] = useState('');


  // 3. tipo de usuario
  const [tipo_usuario, settipo_usuario] = useState<Tipo_Usuario>('');

  // 4. datos por tipo de usuario

  //alumno
  const [num_control, setnum_control] = useState('');
  const [id_carrera, setId_carrera] = useState('');
  const [semestre, setSemestre] = useState('');
  //DOCENTE
  const [num_empleado, setNum_empleado] = useState('');
  const [id_departamento, setId_departamento] = useState('');
  //exalumno
  const [anio_egreso, setAnio_egreso] = useState('');

  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);


  //Filtrar los departamentos por nombre
  const [departamentos, setDepartamentos] = useState<Departamentos[]>([]);
  const [cargandoDepartamentos, setCargandoDepartamentos] = useState(false);

  //Ffiltrar las carreras por nombre
  const [carreras, setCarreras] = useState<Carreras[]>([]);
  const [cargandoCarreras, setCargandoCarreras] = useState(false);

  useEffect(() => {
    const cargarDepartamentos = async () => {
      setCargandoDepartamentos(true);
      try {
        const data = await departamentosService.listar();
        setDepartamentos(data);
      } catch (err) {
        console.error('Error cargando departamentos:', err);
      } finally {
        setCargandoDepartamentos(false);
      }
    };
    cargarDepartamentos();
  }, []);

  useEffect(() => {
    const cargarCarreras = async () => {
      setCargandoCarreras(true);
      try {
        //const data = await carrerasService.listar();
        //setCarreras(data);
        const data = await carrerasService.listar();

        console.log('CARRERAS RECIBIDAS:', data);
        console.log('ES UN ARRAY:', Array.isArray(data));

        setCarreras(data);
      } catch (err) {
        console.error('Error cargando carreras:', err);
      } finally {
        setCargandoCarreras(false);
      }
    };
    cargarCarreras();
  }, []);

  // navegacion entre pasos
  const irAdelante = () => {
    setDireccion('adelante');
    setPaso((p) => (p < 4 ? ((p + 1) as 1 | 2 | 4) : p));
  };

  const irAtras = () => {
    setDireccion('atras');
    setPaso((p) => (p > 1 ? ((p - 1) as 1 | 2 | 3 | 4) : p));
  };

  // validaciones que son necesarias antes de pasar al siguiente paso
  const validarPaso1 = (): boolean => {
    if (
      !correo ||
      !password ||
      !confirmPassword
    ) {
      setError('Todos los campos son obligatorios');
      return false;
    }
    if (password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return false;
    }
    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return false;
    }
    setError('');
    return true;
  };

  const validarPaso2 = (): boolean => {
    if (
      !nombre ||
      !apellido_paterno ||
      !apellido_materno
    ) {
      setError('Todos los campos son obligatorios');
      return false;
    }
    setError('');
    return true;
  };

  const validarPaso3 = (): boolean => {
    if (!tipo_usuario) {
      setError('Selecciona tu tipo de usuario');
      return false;
    }
    setError('');
    return true;
  };

  const validarPaso4 = (): boolean => {
    if (tipo_usuario === 'ESTUDIANTE' && (!num_control || !id_carrera || !semestre)) {
      setError('Completa todos los campos de estudiante');
      return false;
    }
    if (tipo_usuario === 'DOCENTE' && (!num_empleado || !id_departamento)) {
      setError('Completa todos los campos del administrador');
      return false;
    }
    if (tipo_usuario === 'EGRESADO' && !anio_egreso) {
      setError('Completa el año de egreso');
      return false;
    }
    setError('');
    return true;
  };

  // boton para continuar
  const handleSiguiente = () => {
    if (paso === 1 && validarPaso1()) irAdelante();
    else if (paso === 2 && validarPaso2()) irAdelante();
    else if (paso === 3 && validarPaso3()) irAdelante();
  };

  // submit final 
  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validarPaso4()) return;

    setCargando(true);
    setError('');

    const payload: RegistroPayload = {
      nombre,
      apellido_paterno,
      apellido_materno,
      correo,
      password,
      tipo_usuario: tipo_usuario as 'ESTUDIANTE' | 'DOCENTE' | 'EGRESADO',

      // Campos específicos por tipo
      ...(tipo_usuario === 'ESTUDIANTE' && {
        num_control,
        id_carrera: Number(id_carrera),
        semestre: Number(semestre),
      }),
      ...(tipo_usuario === 'DOCENTE' && {
        num_empleado,
        id_departamento: Number(id_departamento),
      }),
      ...(tipo_usuario === 'EGRESADO' && {
        anio_egreso: Number(anio_egreso),
      }),
    };

    try {
      const respuesta = await authService.registrarUsuario(payload);
      console.log('Registro exitoso:', respuesta);

      alert(
        `¡Cuenta creada exitosamente!\n\n` +
        `Usuario: ${respuesta.nombre}\n\n` +
        `Serás redirigido al inicio de sesión.`
      );

      // Redirigir al login con mensaje de éxito
      navigate('/login', {
        state: { mensaje: 'Cuenta creada. Ya puedes iniciar sesión.' },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setCargando(false);
    }
  };

  const animacionPaso = direccion === 'adelante' ? 'animate-slide-left' : 'animate-slide-right';

  return (
    <AuthLayout>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-3 items-center"
      >
        <AuthHeader
          titulo="Crea tu cuenta"
          subtitulo="Únete a la comunidad de investigación del ITCJ"
        />

        {/* {indicador de paso */}
        <IndicadorPasos pasos={4} pasoActual={paso} />

        {/* ─── Contenedor con transición ─── */}
        <AnimacionParte paso={paso} direccion={direccion}>

          {/* 1: Datos digitales*/}
          {paso === 1 && (
            <>

              <Input
                id="correo"
                label="correo"
                type="email"
                value={correo}
                onChange={setcorreo}
                placeholder="tu@correo.com"
                autoComplete="correo"
                required
              />
              <Input
                id="password"
                label="Contraseña"
                type="password"
                value={password}
                onChange={setPassword}
                placeholder="Mínimo 8 caracteres"
                autoComplete="new-password"
                required
              />
              <Input
                id="confirmPassword"
                label="Confirmar contraseña"
                type="password"
                value={confirmPassword}
                onChange={setConfirmPassword}
                placeholder="Repite tu contraseña"
                autoComplete="new-password"
                required
              />
            </>
          )}


          {/* 2. nombrec ompleto */}
          {paso === 2 && (
            <>
              <Input
                id="nombre"
                label="Nombre"
                type="text"
                value={nombre}
                onChange={setNombre}
                placeholder="Juan"
                autoComplete="given-name"
                required
              />
              <Input
                id="apellido_paterno"
                label="Apellido paterno"
                type="text"
                value={apellido_paterno}
                onChange={setapellido_paterno}
                placeholder="Martínez"
                autoComplete="family-name"
                required
              />
              <Input
                id="apellido_materno"
                label="Apellido materno"
                type="text"
                value={apellido_materno}
                onChange={setapellido_materno}
                placeholder="Guzmán"
                autoComplete="additional-name"
                required
              />
            </>
          )}

          {/* 3: Tipo de usuario*/}
          {paso === 3 && (
            <TipoUsuarioRadio value={tipo_usuario} onChange={settipo_usuario} />
          )}

          {/* 4: datos especificos por tipo de usuario*/}
          {paso === 4 && (
            <>
              {tipo_usuario === 'ESTUDIANTE' && (
                <>
                  <Input
                    id="num_control"
                    label="Número de control"
                    type="text"
                    value={num_control}
                    onChange={setnum_control}
                    placeholder="23111531"
                    required
                  />
                  <label htmlFor="id_carrera" className="flex flex-col w-72">
                    <span className="text-sm self-start font-cuerpo font-semibold">
                      Carrera
                    </span>
                    <select
                      id="id_carrera"
                      value={id_carrera}
                      onChange={(e) => setId_carrera(e.target.value)}
                      required
                      disabled={cargandoCarreras}
                      className="bg-[var(--bg)] font-sub-pixel text-[var(--rojo)]
                          px-3 py-1.5 rounded-xl w-full
                          focus:outline-none focus:ring-2 focus:ring-[var(--rosita)]/50
                          transition border-2 border-[var(--negro)] border-r-5 border-b-5
                          cursor-pointer disabled:opacity-50"
                      >
                      <option value="">
                        {cargandoCarreras ? 'Cargando...' : 'Selecciona tu carrera'}
                      </option>
                      {carreras.map((car) => (
                        <option key={car.id_carrera} value={car.id_carrera}>
                          {car.nombre}
                        </option>
                      ))}
                    </select>
                  </label>
                  <Input
                    id="semestre"
                    label="Semestre"
                    type="number"
                    value={semestre}
                    onChange={setSemestre}
                    placeholder="1"
                    required
                  />
                </>
              )}

              {tipo_usuario === 'DOCENTE' && (
                <>
                  <Input
                    id="num_empleado"
                    label="Número de empleado"
                    type="text"
                    value={num_empleado}
                    onChange={setNum_empleado}
                    placeholder="EMP-00123"
                    required
                  />
                  <label htmlFor="id_departamento" className="flex flex-col w-72">
                    <span className="text-sm self-start font-cuerpo font-semibold">
                      Departamento
                    </span>
                    <select
                      id="id_departamento"
                      value={id_departamento}
                      onChange={(e) => setId_departamento(e.target.value)}
                      required
                      disabled={cargandoDepartamentos}
                      className="bg-[var(--bg)] font-sub-pixel text-[var(--rojo)]
                          px-3 py-1.5 rounded-xl w-full
                          focus:outline-none focus:ring-2 focus:ring-[var(--rosita)]/50
                          transition border-2 border-[var(--negro)] border-r-5 border-b-5
                          cursor-pointer disabled:opacity-50"
                      >
                      <option value="">
                        {cargandoDepartamentos ? 'Cargando...' : 'Selecciona un departamento'}
                      </option>
                      {departamentos.map((dep) => (
                        <option key={dep.id_departamento} value={dep.id_departamento}>
                          {dep.nombre}
                        </option>
                      ))}
                    </select>
                  </label>
                </>
              )}

              {tipo_usuario === 'EGRESADO' && (
                <Input
                  id="anio_egreso"
                  label="Año de egreso"
                  type="number"
                  value={anio_egreso}
                  onChange={setAnio_egreso}
                  placeholder="2020"
                  required
                />
              )}
            </>
          )}
        </ AnimacionParte>

        {/* donde aparece el error */}
        {error && (
          <p className="text-xs text-[var(--rosita)] text-center w-72 mt-1">
            {error}
          </p>
        )}

        {/* botones de atras y adelante atra y adelante atras y */}
        <BtnNavegar pasoActual={paso}
          pasoTotal={4}
          onAtras={irAtras}
          onSiguiente={handleSiguiente}
          cargando={cargando}
        />

        {paso === 1 && (
          <AuthFooter
            texto="¿Ya tienes cuenta?"
            linkTexto="Inicia sesión"
            linkTo="/login"
          />
        )}
      </form>
    </AuthLayout>
  );
};

export default FormRegister;  