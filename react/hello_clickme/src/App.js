import React, { Component } from 'react';

class App extends Component {
  state = {
    hello: "Hello App.js!!"
  }

  handleChange = () => {
    this.setState({
      hello: "Bye App.js"
    })
  }
  
  render() {
    return (
      <div className="App">
        <div>{this.state.hello}</div>
        <button onClick={this.handleChange}>Click me!</button>
      </div>
      )
  }
}

export default App;