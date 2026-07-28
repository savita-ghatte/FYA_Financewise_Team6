document.getElementById('calculateBtn').addEventListener('click', function() {
    const incomeInput = document.getElementById('incomeInput').value;
    const income = parseFloat(incomeInput);

    if (isNaN(income) || income <= 0) {
        alert("Please enter a valid monthly income.");
        return;
    }

    // 1. Calculate standard 25% savings and 75% spending budget
    const savings = income * 0.25;
    const spending = income * 0.75;

    // 2. Save values to localStorage for other pages to use
    localStorage.setItem('userIncome', income);
    localStorage.setItem('baseSavings', savings);
    localStorage.setItem('spendingBudget', spending);

    // If no expenses exist yet, initialize an empty array in localStorage
    if (!localStorage.getItem('expenses')) {
        localStorage.setItem('expenses', JSON.stringify([]));
    }

    // 3. Update Home Page Displays
    updateHomeDisplays();
});

function updateHomeDisplays() {
    const income = parseFloat(localStorage.getItem('userIncome')) || 0;
    const savings = parseFloat(localStorage.getItem('baseSavings')) || 0;
    const spending = parseFloat(localStorage.getItem('spendingBudget')) || 0;

    // Calculate total expenses from localStorage
    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    const totalExpenses = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const remaining = spending - totalExpenses;

    document.getElementById('incomeDisplay').innerText = `₹${income.toLocaleString('en-IN')}`;
    document.getElementById('savingDisplay').innerText = `₹${savings.toLocaleString('en-IN')}`;
    document.getElementById('spendingDisplay').innerText = `₹${spending.toLocaleString('en-IN')}`;
    document.getElementById('remainingDisplay').innerText = `₹${remaining.toLocaleString('en-IN')}`;
}

// Automatically load numbers when returning to the Home Page
window.onload = updateHomeDisplays;