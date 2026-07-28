// =======================================
// Saving Goals Quiz Questions
// =======================================

const questions = [

{
question:"Why is setting a saving goal important?",
options:[
"To spend more money",
"To stay focused on future financial needs",
"To increase debt",
"To avoid budgeting"
],
answer:1
},

{
question:"What is an emergency fund?",
options:[
"Money for shopping",
"Money saved for unexpected expenses",
"Money borrowed from a bank",
"Money kept for entertainment"
],
answer:1
},

{
question:"What percentage of your income is commonly recommended for savings?",
options:[
"5%",
"10%",
"20%",
"50%"
],
answer:2
},

{
question:"Which is an example of a short-term saving goal?",
options:[
"Buying groceries",
"Buying a new mobile phone",
"Retirement",
"Buying a house"
],
answer:1
},

{
question:"Which is an example of a long-term saving goal?",
options:[
"Weekend movie",
"Buying snacks",
"Buying a house",
"Ordering food"
],
answer:2
},

{
question:"Which account is best for keeping your savings safely?",
options:[
"Savings Account",
"Current Account",
"Loan Account",
"Credit Card"
],
answer:0
},

{
question:"Which habit helps you achieve your saving goals?",
options:[
"Impulse shopping",
"Saving first before spending",
"Borrowing frequently",
"Ignoring expenses"
],
answer:1
},

{
question:"Why should you save before investing?",
options:[
"To build financial security",
"To increase shopping",
"To avoid taxes",
"To spend freely"
],
answer:0
},

{
question:"Which of these can reduce your savings?",
options:[
"Budgeting",
"Tracking expenses",
"Impulse buying",
"Saving regularly"
],
answer:2
},

{
question:"Achieving your saving goals helps you:",
options:[
"Become financially secure",
"Increase debt",
"Spend more unnecessarily",
"Avoid financial planning"
],
answer:0
}

];

// =======================================
// Variables
// =======================================

let currentQuestion = 0;
let score = 0;

let userAnswers = new Array(questions.length).fill(null);

// =======================================
// HTML Elements
// =======================================

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

// =======================================
// Load Question
// =======================================

function loadQuestion(){

const q = questions[currentQuestion];

question.innerHTML = q.question;

option0.innerHTML = q.options[0];
option1.innerHTML = q.options[1];
option2.innerHTML = q.options[2];
option3.innerHTML = q.options[3];

questionNumber.innerHTML =
`Question ${currentQuestion + 1} of ${questions.length}`;

progress.style.width =
((currentQuestion + 1) / questions.length) * 100 + "%";

// Remove previous selection

document.querySelectorAll('input[name="answer"]').forEach(r=>{

r.checked = false;

});

// Restore saved answer

if(userAnswers[currentQuestion] != null){

document.querySelectorAll('input[name="answer"]')
[userAnswers[currentQuestion]].checked = true;

}

// Previous Button

prevBtn.style.display =
currentQuestion == 0 ? "none" : "inline-block";

// Next & Submit Button

if(currentQuestion == questions.length - 1){

nextBtn.style.display = "none";
submitBtn.style.display = "inline-block";

}
else{

nextBtn.style.display = "inline-block";
submitBtn.style.display = "none";

}

}

// =======================================
// Save Selected Answer
// =======================================

document.querySelectorAll('input[name="answer"]').forEach((radio)=>{

radio.addEventListener("change",()=>{

userAnswers[currentQuestion] = parseInt(radio.value);

});

});

// =======================================
// Load First Question
// =======================================

loadQuestion();
// =======================================
// Previous Button
// =======================================

prevBtn.addEventListener("click", () => {

    if (currentQuestion > 0) {
        currentQuestion--;
        loadQuestion();
    }

});

// =======================================
// Next Button
// =======================================

nextBtn.addEventListener("click", () => {

    if (userAnswers[currentQuestion] == null) {
        alert("Please select an answer before continuing.");
        return;
    }

    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        loadQuestion();
    }

});

// =======================================
// Submit Quiz
// =======================================

submitBtn.addEventListener("click", () => {

    if (userAnswers[currentQuestion] == null) {
        alert("Please select an answer before submitting.");
        return;
    }

    score = 0;

    for (let i = 0; i < questions.length; i++) {

        if (userAnswers[i] === questions[i].answer) {
            score++;
        }

    }

    showResult();

});

// =======================================
// Show Result
// =======================================

function showResult() {

    const percentage = Math.round((score / questions.length) * 100);

    document.querySelector(".quiz-card").style.display = "none";

    document.getElementById("resultBox").style.display = "block";

    document.getElementById("score").innerHTML =
        `Score : ${score} / ${questions.length}`;

    document.getElementById("percentage").innerHTML =
        `Percentage : ${percentage}%`;

    let performance = "";
    let badge = "";

    if (score >= 9) {

        performance = "🏆 Excellent! You are a Saving Goals Expert.";
        badge = "🥇 Badge Earned: Saving Champion";

    }

    else if (score >= 7) {

        performance = "👏 Very Good! You have excellent saving habits.";
        badge = "🥈 Badge Earned: Smart Saver";

    }

    else if (score >= 5) {

        performance = "👍 Good! Keep working towards your saving goals.";
        badge = "🥉 Badge Earned: Future Saver";

    }

    else {

        performance = "📚 Needs Improvement. Learn more about saving and financial planning.";
        badge = "📖 Keep Practicing";

    }

    document.getElementById("performance").innerHTML =
        performance + "<br><br>" + badge;

}

// =======================================
// Restart Quiz
// =======================================

function restartQuiz() {

    currentQuestion = 0;
    score = 0;

    userAnswers = new Array(questions.length).fill(null);

    document.querySelector(".quiz-card").style.display = "block";

    document.getElementById("resultBox").style.display = "none";

    loadQuestion();

}