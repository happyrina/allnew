// import React from 'react';

// function Hello({name, color, isSpecial}) {
//     return (
//     <div style={{ color }}>
//     {isSpecial && <b> * </b>}
//     Hello~!! {name} </div>
//     )
// }

// Hello.defaultProps = {
//     name: 'NoName'
// }


// export default Hello;

import React from 'react';

function Hello({name, color, isSpecial }) {
    return (
        <div style={{ color }}>
        {isSpecial ? <b> * </b> : null}
        Hello~!! { name }</div>
    )
}

Hello.defaultProps = {
    name: 'NoName'
}

export default Hello;