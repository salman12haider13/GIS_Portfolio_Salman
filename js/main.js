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

// Highlight active section in navbar while scrolling
const sectionLinks = document.querySelectorAll(".nav-menu a[href^='#']");
const sections = Array.from(sectionLinks)
  .map((link) => {
    const section = document.querySelector(link.getAttribute("href"));
    return section ? { section, link } : null;
  })
  .filter(Boolean);

function setActiveNavLink() {
  const scrollPosition = window.scrollY + 120;

  let current = sections[0];

  sections.forEach((item) => {
    if (item.section.offsetTop <= scrollPosition) {
      current = item;
    }
  });

  sectionLinks.forEach((link) => link.classList.remove("active"));

  if (current && current.link) {
    current.link.classList.add("active");
  }
}

if (sections.length) {
  window.addEventListener("scroll", setActiveNavLink);
  window.addEventListener("load", setActiveNavLink);
}

// Show more / show fewer project cards
const projectGrid = document.querySelector("#projectGrid");
const toggleProjects = document.querySelector("#toggleProjects");

if (projectGrid && toggleProjects) {
  toggleProjects.addEventListener("click", () => {
    const isExpanded = projectGrid.classList.toggle("expanded");

    toggleProjects.textContent = isExpanded
      ? "Show Fewer Projects ↑"
      : "Show More Projects ↓";
  });
}

// Project filter buttons for older/secondary pages if needed
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

// Homepage map showcase slider
const maps = [
  {
    title: "Paradise Valley Trail Run Routes",
    category: "Terrain / Route Mapping",
    text:
      "A terrain-focused race route map showing 5K and 10K trail routes with elevation, route context, and supporting map elements.",
    focus: "Route design, terrain, elevation profile",
    tools: "ArcGIS Pro, cartographic layout",
    image: "assets/images/maps/previews/paradise-valley-trail-run.jpg",
    story: "maps/paradise-valley-trail-run.html",
    alt: "Paradise Valley Trail Run route map preview"
  },
  {
    title: "Heathrow’s Global Reach",
    category: "Flowline Cartography",
    text:
      "A global aviation flow map showing Heathrow’s international connections using a dark basemap, curved flowlines, and strong visual hierarchy.",
    focus: "Flowlines, global connections, visual hierarchy",
    tools: "ArcGIS Pro, cartographic design",
    image: "assets/images/maps/previews/heathrow-global-reach.jpg",
    story: "maps/heathrow-global-reach.html",
    alt: "Heathrow global reach flowline map preview"
  },
  {
    title: "Calgary Park Accessibility",
    category: "Urban GIS / Accessibility",
    text:
      "An urban GIS map exploring park accessibility and social deprivation patterns in Calgary, designed for planning and equity-focused interpretation.",
    focus: "Accessibility, social deprivation, urban planning",
    tools: "ArcGIS Pro, spatial analysis",
    image: "assets/images/maps/previews/calgary-park-accessibility.jpg",
    story: "maps/calgary-park-accessibility.html",
    alt: "Calgary park accessibility map preview"
  },
  {
    title: "Flood Affected Settlements of Chiniot",
    category: "Disaster Mapping",
    text:
      "A flood impact map showing affected settlements, district context, satellite imagery, and supporting location information for disaster mapping.",
    focus: "Flood impact, settlements, satellite imagery",
    tools: "ArcGIS Pro, remote sensing context",
    image: "assets/images/maps/previews/flood-affected-settlements.jpg",
    story: "maps/flood-affected-settlements.html",
    alt: "Flood affected settlements of Chiniot map preview"
  }
];

let currentMapIndex = 0;

const mapImage = document.querySelector("#mapShowcaseImage");
const mapCategory = document.querySelector("#mapShowcaseCategory");
const mapTitle = document.querySelector("#mapShowcaseTitle");
const mapText = document.querySelector("#mapShowcaseText");
const mapFocus = document.querySelector("#mapShowcaseFocus");
const mapTools = document.querySelector("#mapShowcaseTools");
const mapStory = document.querySelector("#mapShowcaseStory");
const prevMap = document.querySelector("#prevMap");
const nextMap = document.querySelector("#nextMap");
const mapThumbButtons = document.querySelectorAll(".map-thumb-button");

function updateMapShowcase(index) {
  if (!mapImage || !mapCategory || !mapTitle || !mapText || !mapFocus || !mapTools || !mapStory) {
    return;
  }

  const selectedMap = maps[index];
  const preview = mapImage.closest(".map-story-preview");

  if (preview) {
    preview.classList.remove("image-missing");
  }

  mapImage.style.display = "block";
  mapImage.src = selectedMap.image;
  mapImage.alt = selectedMap.alt;
  mapCategory.textContent = selectedMap.category;
  mapTitle.textContent = selectedMap.title;
  mapText.textContent = selectedMap.text;
  mapFocus.textContent = selectedMap.focus;
  mapTools.textContent = selectedMap.tools;
  mapStory.href = selectedMap.story;

  mapThumbButtons.forEach((button) => {
    const buttonIndex = Number(button.dataset.mapIndex);

    if (buttonIndex === index) {
      button.classList.add("active");
    } else {
      button.classList.remove("active");
    }
  });
}

if (prevMap && nextMap && mapThumbButtons.length) {
  prevMap.addEventListener("click", () => {
    currentMapIndex = (currentMapIndex - 1 + maps.length) % maps.length;
    updateMapShowcase(currentMapIndex);
  });

  nextMap.addEventListener("click", () => {
    currentMapIndex = (currentMapIndex + 1) % maps.length;
    updateMapShowcase(currentMapIndex);
  });

  mapThumbButtons.forEach((button) => {
    button.addEventListener("click", () => {
      currentMapIndex = Number(button.dataset.mapIndex);
      updateMapShowcase(currentMapIndex);
    });
  });
}