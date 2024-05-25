import React, { useState } from 'react';
import api from '../../service/BaseUrlApi';

function RegistraUsuario() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await api.post('/api/v1/usuarios/', formData);
      console.log('Server response:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-md">
      <div className="flex flex-col items-center">
        <div className="bg-secondary-main p-2 rounded-full mb-4">
          {/* Substitua com um ícone ou imagem */}
        </div>
        <h1 className="text-lg font-semibold mb-4">Sign up</h1>
        <form className="w-full" onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 gap-2">
            <div className="md:flex md:space-x-2">
              <input className="p-2 border border-gray-300 rounded w-full mb-2 md:mb-0" type="text" name="firstName" placeholder="First Name" required onChange={handleInputChange} />
              <input className="p-2 border border-gray-300 rounded w-full" type="text" name="lastName" placeholder="Last Name" required onChange={handleInputChange} />
            </div>
            <input className="p-2 border border-gray-300 rounded w-full mb-2" type="text" name="username" placeholder="Username" required onChange={handleInputChange} />
            <input className="p-2 border border-gray-300 rounded w-full mb-2" type="email" name="email" placeholder="Email Address" required onChange={handleInputChange} />
            <input className="p-2 border border-gray-300 rounded w-full mb-2" type="password" name="password" placeholder="Password" required onChange={handleInputChange} />
          </div>
          <button className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4" type="submit">Sign Up</button>
          <div className="text-right mt-2">
            <a href="/" className="text-blue-500 hover:underline">Já tem uma conta? Entrar</a>
          </div>
        </form>
      </div>
    </div>
  );
}

export default RegistraUsuario;
