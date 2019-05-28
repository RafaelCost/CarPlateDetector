import React,{Component} from 'react';
import ReactDOM from 'react-dom';


class Display extends Component{
    constructor(props) {
       super(props);
       this.state ={
           accepted_predict:false
       }
       this.onFormSubmit = this.onFormSubmit.bind(this)
       this.onChange = this.onChange.bind(this)
       this.fileUpload = this.fileUpload.bind(this)
     }

     onFormSubmit(e){
         e.preventDefault() // Stop form submit
         this.fileUpload(this.state.file).then((response)=>{
           console.log(response.data);

         })
      }
     onChange(e) {
         this.setState({file:e.target.files[0]})
         this.setState({imageShow: URL.createObjectURL(e.target.files[0])})
         this.setState({image:URL.createObjectURL(e.target.files[0])})
     }
    fileUpload(file){
         const url = 'http://localhost:5000/savePlate';
         const formData = new FormData();
         formData.append('image',this.props.file)
         formData.append('plate',this.props.plate)
         formData.append('accepted_predict',this.props.aprovate)

         const config = {
             headers: {
                 'content-type': 'multipart/form-data'
             }
         }
         return  post(url, formData,config)
     }

     render(){
        return(
          <div>

          <p className="h2 text-center">Imagem</p>
            {this.props.image &&
                <img className = "mg-fluid img-thumbnail mw-80" src={this.props.image} alt="Logo" />
            }


            {this.props.plate &&


                <div className = "row">
                <div className = "col">
                <p className = 'h4 p-2'>Placa: {this.props.plate}</p>
                </div>
                <div className = "col">
                <button type="button" class="btn btn-success">Acertou</button>
                <button type="button" class="btn btn-danger"> Errou </button>
                </div>
                </div>
            }






          </div>
      );
    }
}

export default Display
