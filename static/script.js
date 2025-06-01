let display = document.getElementById('display');
let historyList = document.getElementById('history-list');
let historyPanel = document.getElementById('history-panel');
let current = "";
let operand1 = null;
let operator = null;

function press(val) {
    current += val;
    display.value += val;
}

function clearDisplay() {
    current = "";
    operand1 = null;
    operator = null;
    display.value = "";
}

function setOperator(op) {
    if (current === "" && display.value === "") return;

    // Check if last character is an operator
    const lastChar = display.value.slice(-1);
    if (["+", "-", "*", "/"].includes(lastChar)) {
        // Replace last operator with new one
        display.value = display.value.slice(0, -1) + op;
        operator = op;
    } else {
        operand1 = current;
        operator = op;
        display.value += op;
        current = "";
    }
}

function calculate() {
    if (operand1 === null || operator === null || current === "") return;
    fetch('/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            operand1: operand1,
            operand2: current,
            operator: operator
        })
    })
    .then(res => res.json())
    .then(data => {
        display.value = data.result;
        operand1 = null;
        operator = null;
        current = "";
        if (historyPanel.style.display !== "none") {
            loadHistory();
        }
    });
}

function toggleHistory() {
    if (historyPanel.style.display === "none") {
        historyPanel.style.display = "block";
        loadHistory();
    } else {
        historyPanel.style.display = "none";
    }
}

function loadHistory() {
    fetch('/history')
    .then(res => res.json())
    .then(data => {
        historyList.innerHTML = '';
        data.history.forEach(item => {
            let li = document.createElement('li');
            li.textContent = `${item[0]} = ${item[1]}`;
            historyList.appendChild(li);
        });
    });
}

// Do not show history on load
window.onload = () => {
    historyPanel.style.display = "none";
};