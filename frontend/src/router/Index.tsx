import SignRoutes from './SignRoutes';
import OtherRoutes from './OtherRoutes';
import { BrowserRouter } from 'react-router-dom';
import { useAuth } from '../context/Auth';

const Routes: React.FC = () => {

  const { signed } = useAuth();

  return(
    <BrowserRouter>
      { signed ? <OtherRoutes /> : <SignRoutes /> }
    </BrowserRouter>
  ) 
};

export default Routes;