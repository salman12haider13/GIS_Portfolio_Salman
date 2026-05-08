// Main JavaScript for Salman Haider's GIS portfolio

const navToggle = document.querySelector("#navToggle");
const navMenu = document.querySelector("#navMenu");

if (navToggle && navMenu) {
  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("active");
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

// Close mobile menu after clicking a navigation link
const navLinks = document.querySelectorAll(".nav-menu a");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    if (navMenu && navToggle) {
      navMenu.classList.remove("active");
      navToggle.setAttribute("aria-expanded", "false");
    }
  });
});

// Project filter buttons for projects.html
const filterButtons = document.querySelectorAll(".filter-btn");
const filterItems = document.querySelectorAll("[data-category]");

if (filterButtons.length && filterItems.length) {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const selectedFilter = button.dataset.filter;

      filterButtons.forEach((btn) => btn.classList.remove("active"));
      button.classList.add("active");

      filterItems.forEach((item) => {
        const categories = item.dataset.category.split(" ");

        if (selectedFilter === "all" || categories.includes(selectedFilter)) {
          item.classList.remove("is-hidden");
        } else {
          item.classList.add("is-hidden");
        }
      });
    });
  });
}