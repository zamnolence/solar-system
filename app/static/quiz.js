const MAX_ATTEMPTS = 3;

/* Function for Next button */
function showNextQ(qNum) {
    $(`#Q${parseInt(qNum)+1}Button`).click();
}

/* Function for Previous button */
function showPreviousQ(qNum) {
    $(`#Q${parseInt(qNum)-1}Button`).click();
}

/**
 * Function to validate answer
 * @param {int} qNum tag use as parameter function
**/
function validateMCQ(qNum) {
    let selector =  `input[name=Q${qNum}]:checked`
    let userAnswer = (document.querySelector(selector) || {}).value
    let correctAnswer = document.getElementById('answer'+qNum).innerHTML;

    $('#Q'+qNum+'Button').removeClass('clicked');
    

    /* Handle correct answer */
    if (userAnswer == correctAnswer) {
        
        /* Show message and change color of question button */
        let sideButton = document.getElementById('Q'+qNum+'Button');
        let message = document.getElementById('msg'+qNum);
        sideButton.style.backgroundColor = 'limegreen';
        message.innerHTML = "Correct!";
        updatePoints(qNum, true); /* Update score */

    } else {
        /* Do the same for incorrect answer */
        let sideButton = document.getElementById('Q'+qNum+'Button');
        let message = document.getElementById('msg'+qNum);
        sideButton.style.backgroundColor = 'orange';
        message.innerHTML = `<b>Correct answer is: </b> ${answer}`;
        updatePoints(qNum, false); /* Update score */
    }
    disableMCQButton(qNum);
}

function updatePoints(qNum, isQuestionCorrect) {
    let points = document.getElementById('points').querySelector('b');
    let attemptNum = document.getElementById('attempts'+qNum).innerHTML;
    if (attemptNum==0 && isQuestionCorrect) {
        points.innerHTML = parseInt(points.innerHTML) + 20; /* 20 points for each questions */
        return;
    }
}


function incrementAttempts(qNum) {
    return ++document.getElementById('attempts'+qNum).innerHTML;
}

function disableButton(qNum) {
    let button = document.getElementById('ans'+qNum).querySelector('button');
    button.style.display = 'none';
}

function disableMCQButton(qNum) {
    document.getElementById('mcq'+qNum).querySelector('button').style.display = 'none';
}



/**
 * Function to validate the user input and check the answer
 * @param {String} qNum - Question Number 
 */
function validateAns(qNum) {
    // $.get('/loadquiz?questionsetID=' + questionsetID, function(questions, status) {
    // Gets the user input for the question
    let currentAns = document.getElementById('ans'+qNum).querySelector('input').value.toLowerCase();
    let answer = document.getElementById('answer'+qNum).innerHTML;
    let location = document.getElementById('reference'+qNum).innerHTML;
    if (location == 'None') {
        location = answer;
    }

    // Check if the answer field is empty and alter the user
    if (currentAns == '') {
        alert("Please enter your answer!");
        return;
    }
    else {
        numAttempts = incrementAttempts(qNum);
        let setZoom = zoomOptions[numAttempts-1];
        let setRadius = radiusOptions[numAttempts-1];
        if (currentAns == answer.toLowerCase()) {
            getMapWithMarker(qNum, location, setZoom, setRadius);
            correctAns(qNum);
            removeClassName(qNum);
            disableButton(qNum);
        }
        else {
            if (numAttempts == MAX_ATTEMPTS) {
                getMapWithMarker(qNum, location, setZoom, setRadius);
                wrongAns(qNum, answer);
                disableButton(qNum);
            }
            else {       
                getMapWithRadius(qNum, location, setZoom, setRadius);
                wrongAttempt(qNum, numAttempts);
                if (numAttempts == 1) {
                    removeClassName(qNum);
                }
            }  
        }   
    }
}

function removeClassName(qNum) {
    let element = document.getElementById(`Q${qNum}`).querySelector(".endOfDiv").classList;
    element.remove('endOfDiv');
}

/* AJAX call currently available. Debugging.... */
function submitQuiz() {
    let points = document.getElementById('points').querySelector('b');
    points.innerHTML = parseInt(parseInt(points.innerHTML) * parseFloat(multiplier));
    
    let res_dict = {userID: userID,
                    questionsetID: questionsetID,
                    score: points.innerHTML
                    }
    res_dict = JSON.stringify(res_dict);
    $.ajax({
        type: "POST",
        url: '/submit-results',
        data: res_dict,
        error: function (jqXHR, textStatus, errorThrown) {
             console.log(textStatus); 
            },
        success: function(data, textStatus) {
            let link = 'result';
            window.location.href = link;
        }
    })
}





