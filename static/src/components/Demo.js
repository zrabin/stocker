import React, { Component } from 'react';

export class Demo extends Component {

  constructor(props) {
    super(props);
    this.state = {
      color: 'green'
    };
  }

  handleInputChange(e){
    this.setState({
      color: e.target.value
    })
  }

  render(){

    const styles = {
      fontSize: '40px'
    }

    const boxStyles = {
      backgroundColor: this.state.color,
      height: '400px',
      width: '400px'
    }

    return (
      <div>
        <p style={styles}>demo react component</p>

        <div style={boxStyles}>

        </div>
        <input onChange={(e) => this.handleInputChange(e)} type="text"/>
      </div>
    )
  }
}