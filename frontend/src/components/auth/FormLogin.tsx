import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthLayout from './AuthLayout';
import AuthHeader from './AuthHeader';
import AuthFooter from './AuthFooter';
import Input from '../Input';


const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!email || !password) {
      setError('Todos los campos son obligatorios');
      return;
    }

    setError('');
    console.log('Login:', { email, password });
    // TODO: llamar a la API
    // navigate('/dashboard');
  };

  return (
    <AuthLayout>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 items-center"
      >
        <AuthHeader
          titulo="Inicia Sesión"
          subtitulo="¡Bienvenido! Ingresa tus datos para continuar"
        />

        <Input
          id="email"
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          placeholder="tu@correo.com"
          autoComplete="email"
          required
        />

        <Input
          id="password"
          label="Contraseña"
          type="password"
          value={password}
          onChange={setPassword}
          placeholder="•••••••••••"
          autoComplete="current-password"
          required
        />

        {error && (
          <p className="text-xs text-[var(--rosita)] text-right w-72 mt-2">
            {error}
          </p>
        )}

        <button
          type="submit"
          className="btn btn-ng mt-8"
        >
          <span className="btn-tapa">INICIAR SESIÓN</span>
        </button>

        <AuthFooter
          texto="¿No tienes cuenta?"
          linkTexto="Regístrate"
          linkTo="/register"
        />
      </form>
    </AuthLayout>
  );
};

export default Login;