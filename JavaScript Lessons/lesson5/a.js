function hello(name) {
    console.log("Hello " + name + "!");
}

const minus = (a,b) => {
    return a - b;
};

function add(a, b) {
    let result = a + b;
    return `${a} + ${b} = ${result}`
}

const divide = (x, y) => `${x}/${y} = ${(x/y).toFixed(2)}`

const concatonate = (x,y) => `${x}${y}`

console.log(add(11.999,-12.908385));
console.log(concatonate("Race", "car"));