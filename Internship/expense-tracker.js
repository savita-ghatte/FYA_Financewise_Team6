document.addEventListener("DOMContentLoaded", function() {
    // Load expenses immediately when the page opens
    renderExpenses();

    // Listen for the Add Expense button click
    document.getElementById("addExpBtn").addEventListener("click", function() {
        const name = document.getElementById("expName").value.trim();
        const category = document.getElementById("expCategory").value;
        const amount = parseFloat(document.getElementById("expAmount").value);
        const date = document.getElementById("expDate").value || new Date().toISOString().split('T')[0];

        if (!name || isNaN(amount) || amount <= 0) {
            alert("Please enter a valid expense name and amount.");
            return;
        }

        // 1. Fetch existing expenses from localStorage
        const expenses = JSON.parse(localStorage.getItem('expenses')) || [];

        // 2. Create new expense object with a unique ID (using timestamp)
        const newExpense = {
            id: Date.now(),
            name: name,
            category: category,
            amount: amount,
            date: date
        };

        // 3. Save back to localStorage
        expenses.push(newExpense);
        localStorage.setItem('expenses', JSON.stringify(expenses));

        // 4. Clear the input boxes
        document.getElementById("expName").value = "";
        document.getElementById("expAmount").value = "";
        
        // 5. Update the table and cards
        renderExpenses();
    });
});

function renderExpenses() {
    const expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    const spendingBudget = parseFloat(localStorage.getItem('spendingBudget')) || 0;
    const baseSavings = parseFloat(localStorage.getItem('baseSavings')) || 0;

    const tbody = document.getElementById("expenseTableBody");
    tbody.innerHTML = ""; // Clear the table first

    let totalExpenses = 0;

    // Loop through all saved expenses and create table rows
    expenses.forEach(exp => {
        totalExpenses += exp.amount;
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${exp.name}</td>
            <td>${exp.category}</td>
            <td>₹${exp.amount.toLocaleString('en-IN')}</td>
            <td>${exp.date}</td>
            <td>
                <button onclick="deleteExpense(${exp.id})" style="background:#e74c3c; color:white; border:none; border-radius:4px; padding:6px 12px; cursor:pointer;">
                    <i class="fa-solid fa-trash"></i> Delete
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });

    // Calculate Remaining Budget & Potential Savings
    const remainingBudget = spendingBudget - totalExpenses;
    const potentialSavings = baseSavings + (remainingBudget > 0 ? remainingBudget : 0);

    // Update the 4 Summary Cards at the top
    document.getElementById("totalExpDisplay").innerText = `₹${totalExpenses.toLocaleString('en-IN')}`;
    document.getElementById("remBudgetDisplay").innerText = `₹${remainingBudget.toLocaleString('en-IN')}`;
    document.getElementById("baseSavingDisplay").innerText = `₹${baseSavings.toLocaleString('en-IN')}`;
    document.getElementById("potSavingDisplay").innerText = `₹${potentialSavings.toLocaleString('en-IN')}`;
}

// Function to delete an expense by its ID
function deleteExpense(id) {
    let expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    // Keep all expenses EXCEPT the one that matches the ID
    expenses = expenses.filter(exp => exp.id !== id);
    localStorage.setItem('expenses', JSON.stringify(expenses));
    
    // Refresh the table and cards
    renderExpenses(); 
}