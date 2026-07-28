// ===============================
// Questions
// ===============================

const questions = [

{
question:"What is the main purpose of a budget?",

options:[
"Spend more money",
"Plan and manage income and expenses",
"Increase taxes",
"Borrow money"
],

answer:1

},

{
question:"What percentage of your income should you try to save?",

options:[
"5%",
"10%",
"20%",
"50%"
],

answer:2

},

{
question:"Which of these is a necessary expense?",

options:[
"Gaming",
"Luxury Shoes",
"House Rent",
"Vacation"
],

answer:2

},

{
question:"What is an emergency fund?",

options:[
"Shopping Money",
"Savings for unexpected expenses",
"Travel Money",
"Pocket Money"
],

answer:1

},

{
question:"Which investment is generally considered low risk?",

options:[
"Cryptocurrency",
"Stocks",
"Fixed Deposit",
"Trading"
],

answer:2

},

{
question:"What does SIP stand for?",

options:[
"Safe Investment Plan",
"Savings Insurance Policy",
"Systematic Investment Plan",
"Secure Income Program"
],

answer:2

},

{
question:"Why should you track your expenses?",

options:[
"To spend more",
"To understand spending habits",
"To increase taxes",
"To take loans"
],

answer:1

},

{
question:"Which is an example of passive income?",

options:[
"Salary",
"Rental Income",
"Freelancing",
"Overtime"
],

answer:1

},

{
question:"Before investing, you should first:",

options:[
"Buy expensive gadgets",
"Build an emergency fund",
"Take a loan",
"Spend your salary"
],

answer:1

},

{
question:"Which practice improves online financial security?",

options:[
"Share OTP",
"Use same password",
"Enable Two-Factor Authentication",
"Click unknown links"
],

answer:2

}

];

// ===============================
// Variables
// ===============================

let currentQuestion = 0;

let score = 0;

let userAnswers = new Array(questions.length).fill(null);

// ===============================
// HTML Elements
// ===============================

const question = document.getElementById("question");

const option0 = document.getElementById("option0");

const option1 = document.getElementById("option1");

const option2 = document.getElementById("option2");

const option3 = document.getElementById("option3");

const questionNumber = document.getElementById("question-number");

const progress = document.getElementById("progress");

const nextBtn = document.getElementById("nextBtn");

const prevBtn = document.getElementById("prevBtn");

const submitBtn = document.getElementById("submitBtn");

// ===============================
// Load Question
// ===============================

function loadQuestion(){

const q = questions[currentQuestion];

question.innerHTML = q.question;

option0.innerHTML = q.options[0];

option1.innerHTML = q.options[1];

option2.innerHTML = q.options[2];

option3.innerHTML = q.options[3];

// Update Question Number

questionNumber.innerHTML =
`Question ${currentQuestion+1} of ${questions.length}`;

// Progress Bar

progress.style.width =
((currentQuestion+1)/questions.length)*100 + "%";

// Restore Selected Answer

document.querySelectorAll('input[name="answer"]').forEach(r=>{

r.checked = false;

});

if(userAnswers[currentQuestion] != null){

document.querySelectorAll('input[name="answer"]')
[userAnswers[currentQuestion]].checked=true;

}

// Previous Button

prevBtn.style.display =
currentQuestion==0 ? "none":"inline-block";

// Next & Submit Button

if(currentQuestion==questions.length-1){

nextBtn.style.display="none";

submitBtn.style.display="inline-block";

}

else{

nextBtn.style.display="inline-block";

submitBtn.style.display="none";

}

}

// ===============================
// Save Selected Answer
// ===============================

document.querySelectorAll('input[name="answer"]').forEach((radio)=>{

radio.addEventListener("change",()=>{

userAnswers[currentQuestion]=parseInt(radio.value);

});

});

// ===============================
// Load First Question
// ===============================

loadQuestion();
// ===============================
// Previous Button
// ===============================

prevBtn.addEventListener("click", () => {

    if(currentQuestion > 0){

        currentQuestion--;

        loadQuestion();

    }

});

// ===============================
// Next Button
// ===============================

nextBtn.addEventListener("click", () => {

    if(userAnswers[currentQuestion] == null){

        alert("Please select an answer before continuing.");

        return;

    }

    currentQuestion++;

    loadQuestion();

});

// ===============================
// Submit Quiz
// ===============================

submitBtn.addEventListener("click", () => {

    if(userAnswers[currentQuestion] == null){

        alert("Please select an answer before submitting.");

        return;

    }

    score = 0;

    for(let i=0;i<questions.length;i++){

        if(userAnswers[i] === questions[i].answer){

            score++;

        }

    }

    showResult();

});

// ===============================
// Show Result
// ===============================

function showResult(){

    const percentage = (score / questions.length) * 100;

    document.getElementById("resultBox").style.display = "block";

    document.getElementById("score").innerHTML =
        score + " / " + questions.length;

    document.getElementById("percentage").innerHTML =
        "Percentage : " + percentage + "%";

    let performance = "";

    if(score >= 9){

        performance = "🏆 Excellent! You have strong financial knowledge.";

    }

    else if(score >= 7){

        performance = "🥈 Very Good! Keep learning.";

    }

    else if(score >= 5){

        performance = "🥉 Good! You have basic financial knowledge.";

    }

    else{

        performance = "📚 Needs Improvement. Continue learning financial concepts.";

    }

    document.getElementById("performance").innerHTML = performance;

    // Hide Quiz Card

    document.querySelector(".quiz-card").style.display = "none";

}