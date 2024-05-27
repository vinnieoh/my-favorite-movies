import React, { useState, ChangeEvent, FormEvent } from 'react';
import api from '../../service/BaseUrlApi';
import { useNavigate } from 'react-router-dom';

interface FormData {
  email: string;
  password: string;
}

const Login: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [isErr, setIsErr] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();

    try {
      const response = await api.post(
        'http://127.0.0.1:8000/api/v1/usuario/login',
        `username=${formData.email}&password=${formData.password}`,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      
      	//Fazer buscar o usuario por email na api

      console.log(response.data.access_token)

      navigate('/');

    } catch (error) {
      console.error('Error:', error);
      setIsErr(true);
    }
  };

  return (
    <div className="flex h-screen">
      <div
        className="hidden sm:block sm:w-1/3 md:w-1/2 bg-no-repeat bg-center"
        style={{
          backgroundImage: 'url(./src/assets/img/filme_login.png)',
          backgroundSize: '100%' 
        }}
      ></div>
      <div className="w-full sm:w-2/3 md:w-1/2 bg-white">
        <div className="flex flex-col items-center justify-center py-8 px-4">
          <div className="flex items-center justify-center mb-4">
            {/* Substitua com um ícone ou imagem */}
            <div className="w-12 h-12 bg-secondary-main rounded-full"></div>
          </div>
          <h1 className="text-xl font-semibold mb-2">Sign in</h1>
          <form className="w-full max-w-md" onSubmit={handleLogin}>
            <input className="w-full px-3 py-2 border border-gray-300 rounded mt-1 mb-3" type="email" placeholder="Email Address" name="email" value={formData.email} onChange={handleChange} />
            <input className="w-full px-3 py-2 border border-gray-300 rounded mt-1 mb-3" type="password" placeholder="Password" name="password" value={formData.password} onChange={handleChange} />
            <div className="flex items-center justify-between mt-2 mb-4">
              <label className="flex items-center">
                <input type="checkbox" className="form-checkbox" value="remember" />
                <span className="ml-2">Remember me</span>
              </label>
            </div>
            <button className="w-full py-2 px-4 bg-blue-500 hover:bg-blue-700 text-white font-bold rounded mt-3 mb-2" type="submit">Sign In</button>
            <div className="text-center">
              <a href="/registra-usuario" className="text-blue-500 hover:underline">Don't have an account? Sign Up</a>
            </div>
          </form>
          {isErr && <div className="text-red-500 mt-2">Login failed. Please check your credentials and try again.</div>}
        </div>
      </div>
    </div>
  );
};

export default Login;
