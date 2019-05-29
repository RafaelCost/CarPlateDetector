import React,{Component} from 'react';
import ReactDOM from 'react-dom';
import axios, { post } from 'axios';
import Display from './Display'


export default class Upload extends React.Component{

  constructor(props) {
     super(props);
     this.state ={
       file:null,
       plate:'',
       image: null
     }
     this.onFormSubmit = this.onFormSubmit.bind(this)
     this.onChange = this.onChange.bind(this)
     this.fileUpload = this.fileUpload.bind(this)
   }

   onFormSubmit(e){
       e.preventDefault() // Stop form submit
       this.fileUpload(this.state.file).then((response)=>{
         console.log(response.data);
         this.setState({plate:response.data})
       })
    }
   onChange(e) {
       this.setState({file:e.target.files[0]})
       this.setState({image:URL.createObjectURL(e.target.files[0])})
   }
  fileUpload(file){
       const url = 'http://localhost:5000/uploader';
       const formData = new FormData();
       formData.append('file',file)
       console.log(formData)
       const config = {
           headers: {
               'content-type': 'multipart/form-data'
           }
       }
       return  post(url, formData,config)
   }



  render(){
    return(
      <div className="row  h-100 container-fluid">
          <div className=" col-lg-6  text-center position-static border rounded shadow-sm p-3">
              <h1 className="cover-heading">Enviar Imagem</h1>
              <p className="lead">É necessário enviar uma foto para que nossos algoritmos façam o reconhecimento da placa. </p>
              <form className="md-form" onSubmit={this.onFormSubmit}>
                  <input className="file-path-wrapper" type = "file" name = "image" onChange={this.onChange}/>
                  <p className="lead p-3">
                  <button className="btn btn-lg btn-secondary" type="submit">ENVIAR</button>
                  </p>
              </form>
          </div>

      <div className="col-6 border col-fixed p-3">
        <Display image={this.state.image} plate={this.state.plate}/>
      </div>
      </div>

  );
  }
}
