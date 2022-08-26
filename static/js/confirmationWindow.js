const confirmWindow = document.querySelector(".confirm-window-container");
const openButton = document.querySelector(".open-window");
const closeButtons = document.querySelectorAll(".close-window");

openButton.addEventListener("click", () => {
  confirmWindow.style.display = "block";
});

closeButtons.forEach(closeButton => closeButton.addEventListener("click", () => {
  confirmWindow.style.display = "none";
}));

window.addEventListener("click", (e) => {
  if (e.target.className === "confirm-content-container") {
    e.target.style.display = "none";
  }
});
