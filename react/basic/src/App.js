import React from 'react';
import Hello from './Hello';
import Wrapper from './Wrapper';

function App() {
  return (
    <Wrapper>
    <Hello name="react" color="red" isSpecial={true} />
    <Hello color="pink" />
    </Wrapper>
  )
}

export default App;

// import React from 'react';
// import Hello from './Hello';
// import Wrapper from './Wrapper';

// function App() {
//   return (
//     <Wrapper>
//     <Hello name="react" color="red" isSpecial />
//     <Hello color="pink" />
//     </Wrapper>
//   )
// }

// export default App;

// ## src/App.js inputSample.js

// import React from 'react';
// import InputSample from './InputSample';

// function App() {
//   return (
//     <InputSample />
//   )
// }

// export default App;

//Multi Input State - inputSample.js
// import React from 'react';
// import InputSample from './InputSample';

// function App() {
//   return (
//     <InputSample />
//   )
// }

// export default App;
