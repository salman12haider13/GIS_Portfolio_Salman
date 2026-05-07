// Main JavaScript for the GIS portfolio demo

const navToggle = document.querySelector("#navToggle");
const navMenu = document.querySelector("#navMenu");

navToggle.addEventListener("click", () => {
  navMenu.classList.toggle("active");
});

// Close mobile menu after clicking a link
const navLinks = document.querySelectorAll(".nav-menu a");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    navMenu.classList.remove("active");
  });
});
