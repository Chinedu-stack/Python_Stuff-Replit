let homework = false;
let tired = false;

if (homework && !tired) {
    console.log("You must do you homework now. You are not tired");
} else if (tired && homework) {
    console.log("Okay do you have HW tmr but you are very tired. Get some rest and do it tommorow");
} else {
    console.log("Lucky you. No homework for you!!! Go and do whatever you want.");
}