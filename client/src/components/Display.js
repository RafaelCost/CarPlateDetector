import React,{Component} from 'react';
import ReactDOM from 'react-dom';


class Display extends Component{

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
