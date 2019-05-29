import React,{Component} from 'react';
import ReactDOM from 'react-dom';
import axios, {post,get} from 'axios';


export default class Display extends React.Component{
    constructor(props) {
       super(props);
       this.state ={
           accepted_predict:false,
           file:null,
           plate: ''
       }
       this.onFormSubmit = this.onFormSubmit.bind(this)
       this.onChange = this.onChange.bind(this)
       this.fileUpload = this.fileUpload.bind(this)
     }

     onFormSubmit(e){
         e.preventDefault() // Stop form submit
         this.fileUpload(this.state.accepted_predict).then((response)=>{
           console.log(response.data);
           this.setState({plate:response.data})
         })
      }
     onChange(e) {
         if(e.currentTarget.value == 'SIM'){
            this.setState({accepted_predict:true})
        }else{
            this.setState({accepted_predict:false})
        }
         console.log(e.currentTarget.value)


     }
    fileUpload(acc){
         const url = 'http://localhost:5000/savePlate';
         const config = {
             headers: {
                 'content-type': 'multipart/form-data'
             }
         }
         return  post(url, {'value': acc})
     }


     render(){
        return(
          <div>

          <p className="h2 text-center">Imagem</p>
            {this.props.image &&
                <img className = "mg-fluid img-thumbnail mw-80" src={this.props.image} alt="Logo" />
            }


            {this.props.plate &&

                <div className="row d-flex justify-content-center mt-4">
                    <div className = "row container-fluid text-center" >
                        <h5>A foto acima corresponde a placa: </h5>
                        <h5> {this.props.plate}</h5>
                    </div>


                    <form className="md-form" onSubmit={this.onFormSubmit}>
                            <label><input className= "radio" type="radio" name="optradio" value='SIM' onChange={this.onChange}/>SIM</label>
                            <label><input className= "radio ml-3" type="radio" name="optradio" value='NAO' onChange={this.onChange}/>NÃO</label>
                        <button className="btn btn-secondary ml-3" type="submit">Enviar Resposta</button>
                    </form>
                </div>
            }

          </div>
      );
    }
}
