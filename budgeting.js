// ===============================
// Budgeting Quiz Questions
// ===============================

const questions = [

{
question:"What is the main purpose of a budget?",
options:[
"Spend more money",
"Plan income and expenses",
"Take loans",
"Avoid saving"
],
answer:1
},

{
question:"Which budgeting rule recommends 50% for needs, 30% for wants, and 20% for savings?",
options:[
"70-20-10 Rule",
"50-30-20 Rule",
"80-20 Rule",
"Zero Budget Rule"
],
answer:1
},

{
question:"Which of the following is considered a 'Need'?",
options:[
"Vacation",
"Gaming Console",
"House Rent",
"Luxury Watch"
],
answer:2
},

{
question:"A budget helps you to:",
options:[
"Spend more money",
"Control your spending",
"Increase debt",
"Avoid saving"
],
answer:1
},

{
question:"Which expense should be given the highest priority?",
options:[
"Shopping",
"Electricity Bill",
"Movie Tickets",
"Entertainment"
],
answer:1
},

{
question:"What should you do if your expenses are higher than your income?",
options:[
"Ignore it",
"Reduce unnecessary expenses",
"Spend more",
"Take loans every month"
],
answer:1
},

{
question:"How often should you review your budget?",
options:[
"Once a year",
"Only when you have extra money",
"Regularly every month",
"Never"
],
answer:2
},

{
question:"Which tool is commonly used for creating a budget?",
options:[
"Calculator",
"Budget Planner",
"Camera",
"Music Player"
],
answer:1
},

{
question:"Budgeting mainly develops:",
options:[
"Gaming Skills",
"Financial Discipline",
"Cooking Skills",
"Sports Skills"
],
answer:1
},

{
question:"Budgeting helps you achieve:",
options:[
"More Debt",
"Financial Goals",
"More Expenses",
"Lower Income"
],
answer:1
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

questionNumber.innerHTML =
`Question ${currentQuestion+1} of ${questions.length}`;

progress.style.width =
((currentQuestion+1)/questions.length)*100 + "%";

// Clear selection

document.querySelectorAll('input[name="answer"]').forEach(r=>{

r.checked=false;

});

// Restore previous answer

if(userAnswers[currentQuestion]!=null){

document.querySelectorAll('input[name="answer"]')
[userAnswers[currentQuestion]].checked=true;

}

// Previous Button

prevBtn.style.display =
currentQuestion==0 ? "none":"inline-block";

// Next & Submit

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

    for(let i = 0; i < questions.length; i++){

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

    const percentage = Math.round((score / questions.length) * 100);

    document.getElementById("resultBox").style.display = "block";

    document.getElementById("score").innerHTML =
        score + " / " + questions.length;

    document.getElementById("percentage").innerHTML =
        "Percentage : " + percentage + "%";

    let performance = "";
    let badge = "";

    if(score >= 9){

        performance = "🏆 Excellent! You are a Budgeting Expert.";
        badge = "🏅 Budget Master";

    }

    else if(score >= 7){

        performance = "🥈 Very Good! You have strong budgeting skills.";
        badge = "🥈 Smart Planner";

    }

    else if(score >= 5){

        performance = "🥉 Good! Keep improving your budgeting knowledge.";
        badge = "🥉 Budget Beginner";

    }

    else{

        performance = "📚 Needs Improvement. Continue learning about budgeting.";
        badge = "📖 Learner";

    }

    document.getElementById("performance").innerHTML = performance;

    // Add Badge

    const badgeElement = document.createElement("p");
    badgeElement.innerHTML = "<strong>Badge Earned:</strong> " + badge;
    badgeElement.style.marginTop = "15px";
    badgeElement.style.fontSize = "20px";
    badgeElement.style.color = "#2E9E44";

    const resultBox = document.getElementById("resultBox");

    // Prevent duplicate badge when retaking without refresh
    const oldBadge = document.getElementById("badgeText");
    if(oldBadge){
        oldBadge.remove();
    }

    badgeElement.id = "badgeText";
    resultBox.appendChild(badgeElement);

    // Hide Quiz Card
    document.querySelector(".quiz-card").style.display = "none";

}