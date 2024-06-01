import { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import api from '../service/BaseUrlApi'

interface AuthProviderProps {
  children: ReactNode;
}

interface UserData {
  id: string;
  username: string;
  email: string;
  token: string;
}

interface AuthContextData {
  signed: boolean;
  user: UserData | null;
  LoginApi(data: { email: string; password: string }): Promise<void>;
  Logout(): void;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserData | null>(null);
  const [signed, setSigned] = useState<boolean>(false);

  useEffect(() => {
    const storagedUser = localStorage.getItem('@App:user');
    const storagedToken = localStorage.getItem('@App:token');

    if (storagedUser && storagedToken) {
      setUser(JSON.parse(storagedUser));
      api.defaults.headers.Authorization = `Bearer ${storagedToken}`;
      setSigned(true); // Usuário está autenticado
    }
  }, []);

  async function LoginApi(data: { email: string; password: string }): Promise<void> {
    try {
      const response = await api.post(
        '/usuario/login',
        `username=${data.email}&password=${data.password}`,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      setUser(response.data);
      api.defaults.headers.Authorization = `Bearer ${response.data.token}`;

      localStorage.setItem('@App:user', JSON.stringify(response.data));
      localStorage.setItem('@App:token', JSON.stringify(response.data.token));

      setSigned(true); // Usuário está autenticado
    } catch (error) {
      console.error('Erro ao fazer login:', error);
    }
}

  function Logout() {
    setUser(null);
    localStorage.removeItem('@App:user');
    localStorage.removeItem('@App:token');
    setSigned(false); // Usuário não está mais autenticado
  }

  return (
    <AuthContext.Provider value={{ signed, user, LoginApi, Logout }}>
      {children}
    </AuthContext.Provider>
  );
};

//signed: Boolean(true)

export function useAuth() {
  const context = useContext(AuthContext);
  return context;
}
