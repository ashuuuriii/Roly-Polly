const dropdownButton = document.querySelector(".dropbtn");
dropdownButton.addEventListener("click", toggleDropdown);

function toggleDropdown() {
  document.querySelector(".dropdown-content").classList.toggle("show");
}

// Close dropdown menu when the user clicks outside of menu area
window.onclick = function (e) {
  if (!e.target.matches(".dropbtn")) {
    const dropdownItems = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdownItems.length; i++) {
      const openDropdown = dropdownItems[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};
