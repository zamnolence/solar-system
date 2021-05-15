/*
 * The scripts below are used for basic timer for quiz page.
 * 
*/

/* Initialise time variables for used in the functions */
 const AVAILABLE_TIME = parseInt(document.getElementById('totalTime').innerHTML);
 let timeLeft = AVAILABLE_TIME;
 let timePassed = 0;
 let timerInterval = null;
 
 document.getElementById("timer").innerHTML = 
 `<div id="timer_label" class="timer_label"> ${format_time(timeLeft)} </div>`;
 
 countdown_timer();

/* Countdown timer */
 function countdown_timer() {
    timerInterval = setInterval(() => {
        timePassed += 1;
        timeLeft = AVAILABLE_TIME - timePassed;
        document.getElementById("timer_label").innerHTML = format_time(timeLeft);
        if (timeLeft === 0) {
            clearInterval(timerInterval);
            submitResults();   /* submit result when time runs out */
        }
    }, 1000);
 }


 function format_time(time) {
    const minutes = Math.floor(time / 60);
    let seconds = time % 60;
    if (seconds < 10) {
        seconds = `0${seconds}`;
    }
    return `${minutes}:${seconds}`;
}