const modal = document.querySelector(".modal-container");
const openButton = document.querySelector(".modal-open");
const closeButton = document.querySelector(".modal-close");

openButton.addEventListener("click", () => {
  modal.style.display = "block";
});

closeButton.addEventListener("click", () => {
  modal.style.display = "none";
});

window.addEventListener("click", (e) => {
  if (e.target.className === "modal-container") {
    e.target.style.display = "none";
  }
});
