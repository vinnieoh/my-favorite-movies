import React from 'react';
import {Route, Routes } from 'react-router-dom';
import { Pages } from "../pages/pages";
 

const SignRoutes: React.FC = () => {
  return (  
    <Routes>
      <Route path="/" element={<Pages.Login />} />  
      <Route path="/registra-usario" element={<Pages.RegistraUsuario />} />   
      <Route path="/recupera-senha" element={<Pages.RecuperarSenha />} />  
    </Routes>
  );
};

export default SignRoutes;