document.addEventListener("DOMContentLoaded", function () {
  let currentLog = "api_output.log"; // Default log to display
  const logContentElement = document.getElementById("log-content");

  const apiLogBtn = document.getElementById("api-log-btn");
  const loginLogBtn = document.getElementById("login-log-btn");

  // Function to fetch and display log content
  function fetchLog() {
    fetch(`/logs/${currentLog}`)
      .then((response) => response.text())
      .then((data) => {
        logContentElement.textContent = data;
      })
      .catch((error) => console.error("Error fetching log:", error));
  }

  // Set interval to update log every 2 seconds
  setInterval(fetchLog, 2000);

  // Button event listeners to switch logs
  apiLogBtn.addEventListener("click", function () {
    currentLog = "api_output.log";
    apiLogBtn.classList.add("active");
    loginLogBtn.classList.remove("active");
    fetchLog(); // Fetch immediately when switching
  });

  loginLogBtn.addEventListener("click", function () {
    currentLog = "login_record.log";
    loginLogBtn.classList.add("active");
    apiLogBtn.classList.remove("active");
    fetchLog(); // Fetch immediately when switching
  });

  // Initial log fetch
  fetchLog();
});
