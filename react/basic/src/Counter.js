import React, { useState } from 'react';

function Counter() {
    const [number, setNumber] = useState(0); //앞에변수는 아무거나, 뒤에는 무조건 setNumber로 설정
    
    const onIncrease = () => {
        setNumber(prevNumber => prevNumber + 1);
        console.log('+1')
    }
    const onDecrease = () => {
        setNumber(prevNumber => prevNumber - 1);
        console.log('-1')
    }
    return (
        <div>
        <h1>{number}</h1>
        <button onClick={onIncrease}>+1</button>
        <button onClick={onDecrease}>-1</button>
        </div>
    );
}

export default Counter;