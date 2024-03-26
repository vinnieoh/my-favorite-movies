import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { Pages } from '../pages/pages';
import { Componets } from '../components/componets';

const OtherRoutes: React.FC = () => {
 return (
  <>
    <Componets.Navbar />
    <Routes>
      <Route path="/" element={<Pages.Home/>}/>
      <Route path="/pesquisa-movie" element={<Pages.Search/>}/>
      <Route path="/settings" element={<Pages.Settings/>}/>
      <Route path="/my-movies" element={<Pages.MyMovies/>}/>
    </Routes>
    <Componets.Footer />
  </>
 );
};

export default OtherRoutes;