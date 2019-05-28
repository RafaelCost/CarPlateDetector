import React from 'react';
import logo from './logo.svg';
import './App.css';

//<div className="container-fluid">
//  <nav className="navbar navbar-expand-md navbar-dark bg-dark ">

//    <a className= "navbar-brand" href="#"> RECONHECEDOR DE PLACAS </a>

//    <div className="navbar-nav ml-auto">
//      <a className="nav-item nav-link" href='#'>Home</a>
//      <a className="nav-item nav-link" href='#'>Home</a>
//      <a className="nav-item nav-link" href='#'>Home</a>
//    </div>



//  </nav>
//</div>

import Menu from './components/menu'
import Upload from './components/Upload'

function App() {
  return (

    <div className="row col-lg-12 container-fluid d-flex mh-100 mx-auto flex-column" >
      <header className="row masthead  justify-content-md-center">
          <Menu/>
      </header>
          <Upload />
      
    </div>



  );
}

export default App;
