import { Outlet } from 'react-router-dom';

import Navbar from './components/Navbar';

import { useEffect } from 'react';

function App() {

  useEffect(() => {
    fetch('http://localhost:5000/api') // flask api endpoint
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.log(error));
  }, []);

  return (
    <div>
      <Navbar />
      <main className='container pt-5'>
        <Outlet />
      </main>
    </div>
  );
}

export default App;
