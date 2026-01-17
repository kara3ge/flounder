const terminal = document.getElementById("terminal");
const output = document.getElementById("terminal-output");
const input = document.getElementById("terminal-input-area");
const btn = document.getElementById("terminal-input-submit");


function addTerminalText(text) {
    lineElem = document.createElement('div');
    lineElem.textContent = ">>" + text;
    lineElem.classList.add('terminal-text');
    output.appendChild(lineElem);
    setTimeout(() => {output.scrollTop = output.scrollHeight;}, 0);
}

terminal.addEventListener("submit", (e) => {
    e.preventDefault();

    const command = input.value.trim();
    if (!command) return;
    
    console.log("Command submitted:", command);
    addTerminalText(`$ ${command}`);

    fetch("/api/terminal/command", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({command: command}),
    })
    
    .then(response => {
        console.log("response:", response); 
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(`HTTP error Status: ${response.status} // ${data.error}`);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("data:", data);
        addTerminalText(data.stdout);
    })
    .catch(error => {
        console.error("Error:", error);
        addTerminalText(`Error: ${error.message}`);
    });
    input.value = "";
    input.focus();
});
