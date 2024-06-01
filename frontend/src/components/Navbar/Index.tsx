import { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass, faFilm } from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/Auth'; // Importe o hook useAuth

function Navbar() {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const { Logout } = useAuth(); // Obtenha a função Logout do contexto de autenticação

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogout = () => {
    Logout(); // Chame a função Logout ao clicar em "Sign out"
  };

  return (
    <nav className="bg-white border-gray-200 px-2 sm:px-4 py-2.5 dark:bg-gray-900">
      <div className="container flex flex-wrap justify-between items-center mx-auto">
        <a href="/" className="flex items-center">
          <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">Home</span>
        </a>
        <div className="flex md:order-2">
          <button 
            type="button" 
            className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800" 
            id="user-menu-button" 
            aria-expanded={isDropdownOpen ? "true" : "false"}
            onClick={toggleDropdown}
          >
            <span className="sr-only">Open user menu</span>
            <img className="w-8 h-8 rounded-full" src="./src/assets/img/user_default.jpg" alt="user photo" />
          </button>
          {isDropdownOpen && (
            <div 
              className="z-50 origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none" 
              role="menu" 
              aria-orientation="vertical" 
              aria-labelledby="user-menu-button"
            >
              <div className="py-1">
                <a href="/settings" className="text-gray-700 block px-4 py-2 text-sm">Settings</a>
                <button onClick={handleLogout} className="text-gray-700 block px-4 py-2 text-sm">Sign out</button>
              </div>
            </div>
          )}
        </div>
        <div className="hidden w-full md:flex md:w-auto md:order-1" id="navbar-main">
          <ul className="flex flex-col mt-4 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium">
            <li>
              <a href="/pesquisa-movie" className="block py-2 pr-4 pl-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700">
                <FontAwesomeIcon icon={faMagnifyingGlass} className="inline-block w-4 h-4 mr-1" />
                Search
              </a>
            </li>
            <li>
              <a href="/my-movies" className="block py-2 pr-4 pl-3 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700">
                <FontAwesomeIcon icon={faFilm} className="inline-block w-4 h-4 mr-1" />
                My Movies
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;