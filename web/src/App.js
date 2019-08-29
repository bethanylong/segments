import React from 'react';
import './App.css';

function Rect(props) {
    return (
        <rect fill={props.fill} height={props.height} stroke={props.stroke} width={props.width} x={props.x} y={props.y} />
    );
}

function Line(props) {
    return (
        <line stroke={props.stroke} x1={props.x1} x2={props.x2} y1={props.y1} y2={props.y2} />
    );
}

function SVG(props) {
    return (
        <svg baseProfile="full" height={props.height} version="1.1" width={props.width}>
            <Line stroke="black" x1={props.width / 2} x2={props.width / 2} y1="0" y2={props.height} />
            <Rect fill="none" height="25.0" stroke="green" width="237.5" x="131.25" y="425.0" />
        </svg>
    );
}

function App() {
    return (
        <div>
            <SVG width="500" height="500" />
        </div>
    );
}

export default App;
