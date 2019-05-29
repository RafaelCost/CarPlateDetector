import React from 'react';
import logo from './logo.svg';
import './App.css';

import Menu from './components/menu'
import Upload from './components/Upload'

function App() {
  return (
    <div>

        <header className="row masthead  justify-content-md-center">
            <Menu/>
        </header>
        <div className="row col-lg-12 container-fluid d-flex mh-100 mx-auto flex-column" >
            <Upload />
        </div>
    </div>



  );
}

export default App;
