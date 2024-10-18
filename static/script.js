document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".control-btn");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      const command = this.getAttribute("data-command"); // Get the command from the button
      sendCommand(command); // Send it to the API
    });
  });

  function sendCommand(command) {
    fetch("http://127.0.0.1:10000/move", {
      // Send POST request to the Flask API
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        in_command: [command],
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(`Command sent: ${data.out_command}`);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
