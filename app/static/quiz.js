/*
 * The scripts below are used for generating and operating quiz page, and validating answer.
 * 1. validate_answer() is used for 'Check' button to validate submitted answer
 * 2. handle_correct() and handle_incorrect() are used for prompting user the message
 * 3. update_scores() will increase score for user if correct answer is submitted.
 * 4. nextBtn() and prevBtn() are used for navigating to next or previous question in the set
 * 5. submit_results() is used to AJAX post results (scores and time) to score table and redirect to result page
 * 6. string_to_time() and format_time() are used for time formatting
*/

/**
 * Initialise question number parameter for functions
 * @param {int} qNum - Question number parameter
**/

function validate_answer(qNum) {

    /* get the selected question*/
    let selectQ =  `input[name=Q${qNum}]:checked`
    /* get the corresponding correct answer and user answer from document */
    let correct_ans = document.getElementById('answer'+qNum).innerHTML;
    let user_ans = (document.querySelector(selectQ) || {}).value

    /* Handle correct answer */
    if (user_ans == correct_ans) {
        handle_correct(qNum, true)

    /* Handle incorrect answer*/
    } else {
        handle_incorrect(qNum, false)
    }
    /* Deselect button */
    document.getElementById('mcq'+qNum).querySelector('button').style.display = 'none';
}

function handle_correct(qNum) {
    
    /* Prompt user with coloured message and change button color to limegreen */
    $('#Q'+qNum+'Button').removeClass('clicked');
    let message = document.getElementById('msg'+qNum);
    let qBtn = document.getElementById('Q'+qNum+'Button');
    message.innerHTML = "Correct!";
    message.style.color = 'limegreen';
    qBtn.style.backgroundColor = 'limegreen';

    /* Update score for user*/
    update_scores(qNum, true);

}
function handle_incorrect(qNum, answer) {
    /* Prompt user with coloured message and change button color to limegreen */
    $('#Q'+qNum+'Button').removeClass('clicked');
    let message = document.getElementById('msg'+qNum);
    let qBtn = document.getElementById('Q'+qNum+'Button');
    message.innerHTML = `Incorrect!`;
    message.style.color = 'orange'
    qBtn.style.backgroundColor = 'orange';
    // message.innerHTML = `Correct answer is ${answer}.`;

    /* Update score for user*/
    update_scores(qNum, false);

}

function update_scores(qNum, isCorrect) {
    let points = document.getElementById('points').querySelector('b');
    /* Add scores if isCorrect = true */
    if (isCorrect) {
        points.innerHTML = parseInt(points.innerHTML) + 25;
        return;
    }
    /* Do notting if isCorrect = false*/
}

function nextBtn(qNum) {
    $(`#Q${parseInt(qNum) + 1}Button`).click();
}

function prevBtn(qNum) {
    $(`#Q${parseInt(qNum) - 1}Button`).click();
}

function submit_results() {

    /* Calculate bonus score based on time used*/
    let available_time = parseInt(document.getElementById('totalTime').innerHTML);
    let time_left = string_to_time('timer_label');
    /* multiplier for bonus points is 1 + 0.XX rounded to 2 descimal places */
    let multiplier = (1 + (time_left / available_time)).toFixed(2);
    /* Write message to console */
    console.log(parseFloat(multiplier));
    /* Score = score obtained * multiplier */
    let points = document.getElementById('points').querySelector('b');
    points.innerHTML = parseInt(parseInt(points.innerHTML) * parseFloat(multiplier));

    /* Time used for completing question set */
    timeTaken = available_time - time_left;
    
    /* Return as a dictionary */
    let results_dict = { userID: userID,
                         questionsetID: questionsetID,
                         score: points.innerHTML,
                         timeTaken: format_time(timeTaken)
                        }
    results_dict = JSON.stringify(results_dict); /* Convert */
    
    /* AJAX post results dictionary to submit-result and redirect to result page */
    $.ajax({
        type: "POST",
        url: '/submit-results',
        data: results_dict,
        error: function (jqXHR, textStatus, errorThrown) {
             console.log(textStatus); /* Write status to console if error */
            },
        success: function(data, textStatus) {
            let link = 'result';
            window.location.href = link;
        }
    })
}

function string_to_time(timeID) {
    let timer = document.getElementById(timeID).innerHTML;
    let timeArray = timer.split(":");
    return parseInt(timeArray[0]) * 60 + parseInt(timeArray[1]);
}


function format_time(time) {
    const minutes = Math.floor(time / 60);
    let seconds = time % 60;
    if (seconds < 10) {
        seconds = `0${seconds}`;
    }
    return `${minutes}:${seconds}`;
}


