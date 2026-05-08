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
    title: "Flood Affected Settlements of Chiniot",
    category: "Disaster Mapping",
    text:
      "A flood impact map showing affected settlements, district context, satellite imagery, and supporting location information for disaster mapping.",
    focus: "Flood impact, settlements, satellite imagery",
    tools: "ArcGIS Pro, remote sensing context",
    image: "assets/images/maps/previews/flood-affected-settlements.jpg",
    story: "maps/flood-affected-settlements.html",
    alt: "Flood affected settlements of Chiniot map preview"
  },
  {
    title: "Town of Olds and Surrounding Area",
    category: "Reference Mapping",
    text:
      "A traditional reference map showing the Town of Olds and surrounding area with road hierarchy, water features, railway, inset map, and supporting map elements.",
    focus: "Reference mapping, road hierarchy, inset design",
    tools: "ArcGIS Pro, cartographic layout",
    image: "assets/images/maps/previews/town-of-olds-reference-map.jpg",
    story: "maps/town-of-olds-reference-map.html",
    alt: "Town of Olds and surrounding area reference map preview"
  },
  {
    title: "Red Carpet Community Spatial Overview",
    category: "Urban / Neighbourhood Mapping",
    text:
      "A local-scale community map showing building types, roads, parks, bus stops, and community boundary with a clean inset and neighbourhood-level layout.",
    focus: "Community mapping, urban features, local context",
    tools: "ArcGIS Pro, urban cartography",
    image: "assets/images/maps/previews/red-carpet-community-overview.jpg",
    story: "maps/red-carpet-community-overview.html",
    alt: "Red Carpet community spatial overview map preview"
  },
  {
    title: "Housing Cost in Calgary: DA vs CT",
    category: "Urban GIS / Census Mapping",
    text:
      "A census-based comparison map showing housing costs at dissemination area and census tract scales, useful for explaining spatial aggregation and scale effects.",
    focus: "Housing cost, census geography, DA vs CT comparison",
    tools: "ArcGIS Pro, census mapping",
    image: "assets/images/maps/previews/housing-cost-da-vs-ct.png",
    story: "maps/housing-cost-da-vs-ct.html",
    alt: "Housing cost map comparing dissemination areas and census tracts"
  },
  {
    title: "Calgary Park Accessibility and Social Deprivation",
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
    title: "Friends of Greens Street Tree Planting",
    category: "Environmental / Urban Greening",
    text:
      "A thematic map combining street tree planting counts with tree canopy coverage by Calgary electoral division to support urban greening interpretation.",
    focus: "Tree planting, canopy cover, environmental mapping",
    tools: "ArcGIS Pro, thematic cartography",
    image: "assets/images/maps/previews/friends-of-greens-tree-canopy.jpg",
    story: "maps/friends-of-greens-tree-canopy.html",
    alt: "Friends of Greens street tree planting and tree canopy map preview"
  },
  {
    title: "Stillbirths and Neonatal Deaths in Asia",
    category: "Health Geography",
    text:
      "A health geography map set comparing stillbirths and neonatal deaths in Asia using multiple thematic mapping approaches.",
    focus: "Health outcomes, thematic mapping, Asia",
    tools: "ArcGIS Pro, health geography",
    image: "assets/images/maps/previews/stillbirths-neonatal-deaths-asia.jpg",
    story: "maps/stillbirths-neonatal-deaths-asia.html",
    alt: "Stillbirths and neonatal deaths in Asia map preview"
  },
  {
    title: "Pakistan Rural Household Panel Survey Coverage Map",
    category: "Research / Survey Mapping",
    text:
      "A research-support map showing surveyed districts in Pakistan, designed to communicate geographic coverage for a rural household panel survey.",
    focus: "Survey coverage, administrative mapping, Pakistan",
    tools: "ArcGIS Pro, research mapping",
    image: "assets/images/maps/previews/pakistan-prhps-coverage-map.jpg",
    story: "maps/pakistan-prhps-coverage-map.html",
    alt: "Pakistan Rural Household Panel Survey coverage map preview"
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