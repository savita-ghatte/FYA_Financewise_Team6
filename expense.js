// =======================================
// Expense Tracker Quiz Questions
// =======================================

const questions = [

{
question:"What is an expense tracker?",
options:[
"A shopping website",
"A tool to record income and expenses",
"A social media app",
"A gaming app"
],
answer:1
},

{
question:"Why is tracking expenses important?",
options:[
"To spend more money",
"To understand where your money goes",
"To avoid work",
"To increase debt"
],
answer:1
},

{
question:"Which of the following is a fixed expense?",
options:[
"Movie tickets",
"House Rent",
"Online Shopping",
"Dining Out"
],
answer:1
},

{
question:"Which of the following is a variable expense?",
options:[
"Rent",
"Electricity Bill",
"Insurance Premium",
"Groceries"
],
answer:3
},

{
question:"How often should you record your expenses?",
options:[
"Only once a year",
"Only when shopping",
"Regularly",
"Never"
],
answer:2
},

{
question:"Which expense should you reduce first to save money?",
options:[
"Rent",
"School Fees",
"Impulse Shopping",
"Electricity Bill"
],
answer:2
},

{
question:"An expense tracker helps you:",
options:[
"Spend more",
"Monitor your spending habits",
"Take loans",
"Avoid budgeting"
],
answer:1
},

{
question:"Which category usually contains unnecessary expenses?",
options:[
"Rent",
"Groceries",
"Entertainment",
"Insurance"
],
answer:2
},

{
question:"What is the biggest benefit of tracking expenses?",
options:[
"Higher debt",
"Better financial planning",
"More shopping",
"Higher taxes"
],
answer:1
},

{
question:"Tracking expenses regularly helps you achieve:",
options:[
"Financial stability",
"More debt",
"Higher spending",
"No savings"
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
`Question ${currentQuestion+1} of ${questions.length}`;

progress.style.width =
((currentQuestion+1)/questions.length)*100 + "%";

document.querySelectorAll('input[name="answer"]').forEach(r=>{

r.checked=false;

});

if(userAnswers[currentQuestion]!=null){

document.querySelectorAll('input[name="answer"]')
[userAnswers[currentQuestion]].checked=true;

}

prevBtn.style.display =
currentQuestion==0 ? "none":"inline-block";

if(currentQuestion==questions.length-1){

nextBtn.style.display="none";
submitBtn.style.display="inline-block";

}

else{

nextBtn.style.display="inline-block";
submitBtn.style.display="none";

}

}

// =======================================
// Save Selected Answer
// =======================================

document.querySelectorAll('input[name="answer"]').forEach((radio)=>{

radio.addEventListener("change",()=>{

userAnswers[currentQuestion]=parseInt(radio.value);

});

});

// =======================================
// Load First Question
// =======================================

loadQuestion();
// =======================================
// Previous Button
// =======================================

prevBtn.addEventListener("click",()=>{

if(currentQuestion>0){

currentQuestion--;

loadQuestion();

}

});

// =======================================
// Next Button
// =======================================

nextBtn.addEventListener("click",()=>{

if(userAnswers[currentQuestion]==null){

alert("Please select an answer before continuing.");

return;

}

currentQuestion++;

loadQuestion();

});

// =======================================
// Submit Quiz
// =======================================

submitBtn.addEventListener("click",()=>{

if(userAnswers[currentQuestion]==null){

alert("Please select an answer before submitting.");

return;

}

score=0;

for(let i=0;i<questions.length;i++){

if(userAnswers[i]===questions[i].answer){

score++;

}

}

showResult();

});

// =======================================
// Show Result
// =======================================

function showResult(){

const percentage=Math.round((score/questions.length)*100);

document.querySelector(".quiz-card").style.display="none";

document.getElementById("resultBox").style.display="block";

document.getElementById("score").innerHTML=
`Score : ${score} / ${questions.length}`;

document.getElementById("percentage").innerHTML=
`Percentage : ${percentage}%`;

let performance="";
let badge="";

if(score>=9){

performance="🏆 Excellent! You understand expense tracking very well.";
badge="🥇 Badge Earned : Expense Master";

}

else if(score>=7){

performance="👏 Very Good! You manage expenses wisely.";
badge="🥈 Badge Earned : Smart Spender";

}

else if(score>=5){

performance="👍 Good! Keep tracking your expenses regularly.";
badge="🥉 Badge Earned : Expense Learner";

}

else{

performance="📚 Needs Improvement. Start recording your daily expenses.";
badge="📖 Keep Practicing";

}

document.getElementById("performance").innerHTML=
performance+"<br><br>"+badge;

}

// =======================================
// Restart Quiz
// =======================================

function restartQuiz(){

currentQuestion=0;

score=0;

userAnswers=new Array(questions.length).fill(null);

document.querySelector(".quiz-card").style.display="block";

document.getElementById("resultBox").style.display="none";

loadQuestion();

}