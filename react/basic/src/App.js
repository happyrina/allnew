// import React from 'react';
// import Hello from './Hello';
// // import './App.css';
// import './Wrapper';

// // function App() {
// //   const name = 'react';
// //   const style = {
// //     backgroundColor : "black",
// //     color : 'Hotpink',
// //     fontSize : 24,
// //     padding: '1rem'
// //   }

// //   return (
// //     <div>
// //     <Hello />
// //     <Hello />
// //     <Hello />
// //     <div style={style}>{name}</div>
// //     <div className="gray-box"></div>
// //     </div>
// //     )
// // }

// // function App() {
// //   return (
// //     <Hello name1="react" color="Hotpink" />
// //     <Hello color="blue" />
// //     </>
// //     )
// // }

// function App() {
//   return (
//     <Wrapper>
//     <Hello name1="react" color="red" />
//     <Hello color="pink" />
//     </Wrapper>
//     )
// }


// export default App;

import React from 'react';
import Hello from './Hello';
import Wrapper from './Wrapper';

function App() {
  return (
    <Wrapper>
    <Hello name="react" color="red" />
    <Hello color="pink" />
    </Wrapper>
    )
}

export default App;