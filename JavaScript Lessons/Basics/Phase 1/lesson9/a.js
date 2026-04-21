for (let i = 1; i <=15; i++) {
    if (i % 3 == 0 && i % 5 == 0) {
        console.log(`${i}: divisible by 3 and 5 (FizzBuzz)`);
    } else if (i % 3 == 0) {
        console.log(`${i}: divisible by 3 (Fizz)`);
    } else if (i % 5 == 0) {
        console.log(`${i}: divisible by 5 (Buzz)`);
    } else {
        console.log(`${i}: not divisible by 3 or 5 (not a Fizz, Buzz or FizzBuzz :( )`);
    }
}