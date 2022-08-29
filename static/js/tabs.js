const tabContents = document.querySelectorAll(".tab-content");
const buttons = document.querySelectorAll(".tablinks");

function openTab(e) {
  for (let tabContent of tabContents) {
    tabContent.style.display = "none";
  }

  for (let button of buttons) {
    button.classList.remove("active");
  }

  const targetTab = document.getElementById(e.target.getAttribute("data-key"));
  targetTab.style.display = "block";
  e.target.classList.add("active");
}

buttons.forEach((button) =>
  button.addEventListener("click", (e) => openTab(e))
);
