let palmer = {
    shooting: 84,
    passing: 91,
    physical: 60
};

let list = [1,2,2,3,4];
 
palmer.shooting = 19;

for (let key in palmer) {
    console.log(`${key}: ${palmer[key]}`);
}

console.log(list.length);