import { useState, useEffect, ChangeEvent, FormEvent } from 'react';
import api from '../../service/BaseUrlApi';

interface UserData {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  password?: string;
}

function Settings() {
  const [formData, setFormData] = useState<UserData>({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
  });
  const userId = "id-do-usuario"; // Substitua com o ID real do usuário

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get<UserData>(`/api/v1/usuarios/${userId}`);
        const userData = response.data;
        setFormData({
          firstName: userData.firstName,
          lastName: userData.lastName,
          username: userData.username,
          email: userData.email,
          password: '' // Definindo um valor padrão para 'password'
        });
      } catch (error) {
        console.error('Erro ao buscar dados do usuário:', error);
      }
    };

    fetchUserData();
  }, [userId]);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    // Remova a propriedade 'password' se ela estiver vazia
    const dataToUpdate = formData.password ? formData : { ...formData, password: undefined };

    try {
      const response = await api.put(`/api/v1/usuarios/${userId}`, dataToUpdate);
      console.log('Server response:', response.data);
      alert('Dados atualizados com sucesso!');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-md">
      <h1 className="text-lg font-semibold mb-4">Configurações de Atualizações do Usuário</h1>
      <form className="w-full" onSubmit={handleSubmit}>
        <input className="p-2 border border-gray-300 rounded w-full mb-2" type="text" name="firstName" placeholder="First Name" value={formData.firstName} onChange={handleInputChange} />
        <input className="p-2 border border-gray-300 rounded w-full mb-2" type="text" name="lastName" placeholder="Last Name" value={formData.lastName} onChange={handleInputChange} />
        <input className="p-2 border border-gray-300 rounded w-full mb-2" type="text" name="username" placeholder="Username" value={formData.username} onChange={handleInputChange} />
        <input className="p-2 border border-gray-300 rounded w-full mb-2" type="email" name="email" placeholder="Email Address" value={formData.email} onChange={handleInputChange} />
        <input className="p-2 border border-gray-300 rounded w-full mb-2" type="password" name="password" placeholder="Password" onChange={handleInputChange} />
        <button className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4" type="submit">Atualizar</button>
      </form>
    </div>
  );
}

export default Settings;
