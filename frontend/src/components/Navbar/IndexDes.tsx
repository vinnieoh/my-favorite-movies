import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom'; // Importe o Link para criar o botão de login

function NavbarDes() {
  return (
    <nav className="bg-white border-gray-200 px-2 sm:px-4 py-2.5 dark:bg-gray-900">
      <div className="container flex justify-between items-center mx-auto">
        <Link to="/" className="flex items-center">
          <span className="text-xl font-semibold dark:text-white">Home</span>
        </Link>
        <div className="flex-grow flex justify-center">
          <a href="/pesquisa-movie" className="flex items-center py-2 px-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700">
            <FontAwesomeIcon icon={faMagnifyingGlass} className="w-4 h-4 mr-1" />
            Search
          </a>
        </div>
        <div className="hidden md:flex md:w-auto md:order-1">
          <ul className="flex flex-col mt-4 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium">
            <li>
              <Link to="/login" className="block py-2 px-4 text-gray-700 rounded hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-gray-400 md:dark:hover:text-white dark:hover:bg-gray-700">
                Login
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default NavbarDes;
