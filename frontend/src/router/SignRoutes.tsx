import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { Pages } from '../pages/pages';
import { Componets } from '../components/componets';

const SignRoutes: React.FC = () => {
  return (  
    <>
      <Componets.NavbarDes />
      <Routes>
        <Route path="/" element={<Pages.Home />} />
        <Route path="/movie/:id" element={<Pages.MovieDetail />} />
        <Route path="/tvshow/:id" element={<Pages.TVShowDetail />} />
        <Route path="/pesquisa-movie" element={<Pages.Search/>}/>
        <Route path="/login" element={<Pages.Login />} />
        <Route path="/registra-usuario" element={<Pages.RegistraUsuario />} />
        <Route path="/recupera-senha" element={<Pages.RecuperarSenha />} />
      </Routes>
      <Componets.Footer />
    </>
  );
};

export default SignRoutes;