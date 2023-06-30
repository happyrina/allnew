import React from 'react';

function Hello({name, color}) {
    return <div style={{ color }}>Hello~!! {name} </div>
}

Hello.defaultProps = {
    name: 'NoName'
}


export default Hello;