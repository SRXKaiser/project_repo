import { useState } from 'react';
import type { FormEvent } from 'react';
import AuthLayout from './AuthLayout';
import AuthHeader from './AuthHeader';
import Input from '../Input';
import AuthFooter from './AuthFooter';
import IndicadorPasos from './IndicadorPasos';
import TipoUsuarioRadio from './TipoUserRadio';
import BtnNavegar from './BtnNavegar';
import AnimacionParte from './AnimacionParte';
//import { registrarUsuario } from '../../api/auth';

type Tipo_Usuario = 'ESTUDIANTE' | 'EMPLEADO' | 'EXALUMNO' | '';

const FormRegister = () => {
  const [paso, setPaso] = useState<1 | 2 | 3 | 4>(1);
  const [direccion, setDireccion] = useState<'adelante' | 'atras'>('adelante');

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
    //administrador
  const [num_empleado, setNum_empleado] = useState('');
  const [id_departamento, setId_departamento] = useState('');
    //exalumno
  const [anio_egreso, setAnio_egreso] = useState('');

  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false); 

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
    if (tipo_usuario === 'EMPLEADO' && (!num_empleado || !id_departamento)) {
      setError('Completa todos los campos de empleado');
      return false;
    }
    if (tipo_usuario === 'EXALUMNO' && !anio_egreso) {
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

    // Construir payload con los nombres y tipos que espera el backend
    // const payload = {
    //   nombre,
    //   apellido_paterno,
    //   apellido_materno,
    //   correo: email,                            // email → correo
    //   password,
    //   tipo_usuario: tipo_usuario.toUpperCase(),  // 'estudiante' → 'ESTUDIANTE'
    //   ...(tipo_usuario === 'ESTUDIANTE' && {
    //     num_control,
    //     id_carrera: Number(id_carrera),         // string → number
    //     semestre: Number(semestre),             // string → number
    //   }),
    //   ...(tipo_usuario === 'EMPLEADO' && {
    //     num_empleado,
    //     id_departamento: Number(id_departamento),
    //   }),
    //   ...(tipo_usuario === 'EXALUMNO' && {
    //     anio_egreso: Number(anio_egreso),
    //   }),
    // };

    // try {
    //   const respuesta = await registrarUsuario(payload);
    //   console.log('Registro exitoso:', respuesta);
    //   // TODO: redirigir al login o mostrar mensaje de éxito
    // } catch (err) {
    //   setError(err instanceof Error ? err.message : 'Error desconocido');
    // } finally {
    //   setCargando(false);
    // }
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
        <IndicadorPasos pasos={4} pasoActual={paso}/>

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
                    <Input
                      id="id_carrera"
                      label="Carrera"
                      type="number"
                      value={id_carrera}
                      onChange={setId_carrera}
                      placeholder="Ing. en Sistemas Computacionales"
                      required
                    />
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

                {tipo_usuario === 'EMPLEADO' && (
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
                    <Input
                      id="id_departamento"
                      label="Departamento"
                      type="number"
                      value={id_departamento}
                      onChange={setId_departamento}
                      placeholder="Sistemas y Computación"
                      required
                    />
                  </>
                )}

                {tipo_usuario === 'EXALUMNO' && (
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
          onSiguiente={handleSiguiente} /> 

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