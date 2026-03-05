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

console.log(divide(11, 12))