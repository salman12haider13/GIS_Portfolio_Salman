/* =========================================================
   SALMAN HAIDER — GIS PORTFOLIO SCRIPTS
   Fixed version for kimi-test
   Fixes:
   - Show More Projects
   - Show More Certificates
   - Map thumbnail buttons
   - Safer scroll reveal
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  /* ---------- NAVIGATION ---------- */
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector("#navToggle");
  const menu = document.querySelector("#navMenu");
  const links = document.querySelectorAll(".nav-menu a");

  if (toggle && menu) {
    toggle.addEventListener("click", () => {
      const open = menu.classList.toggle("active");
      toggle.setAttribute("aria-expanded", String(open));
    });

    links.forEach((link) => {
      link.addEventListener("click", () => {
        menu.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  window.addEventListener(
    "scroll",
    () => {
      if (header) header.classList.toggle("scrolled", window.scrollY > 30);
    },
    { passive: true }
  );

  /* ---------- ACTIVE NAV LINK ON SCROLL ---------- */
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');

  function setActive() {
    const y = window.scrollY + 100;
    let current = null;

    sections.forEach((section) => {
      if (section.offsetTop <= y) {
        current = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.toggle("active", link.getAttribute("href") === `#${current}`);
    });
  }

  if (sections.length) {
    window.addEventListener("scroll", setActive, { passive: true });
    window.addEventListener("load", setActive);
    setActive();
  }

  /* ---------- SCROLL REVEAL ---------- */
  const reveals = document.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("active");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );

    reveals.forEach((element) => revealObserver.observe(element));
  } else {
    reveals.forEach((element) => element.classList.add("active"));
  }

  /* ---------- PROJECT TOGGLE: SHOW NEXT 6 ---------- */
  setupIncrementalProjects();

  /* ---------- MAP SHOWCASE ---------- */
  setupMapShowcase();

  /* ---------- CERTIFICATES TOGGLE: SHOW NEXT 6 ---------- */
  setupIncrementalCertificates();

  /* ---------- CONSOLE GREETING ---------- */
  console.log(
    "%c🗺️  Salman Haider — GIS Portfolio",
    "font-size:16px;font-weight:bold;color:#2d5a3d;"
  );
  console.log("%cHiring managers: this portfolio was built with care.", "color:#78716c;");
});

/* =========================================================
   PROJECTS
   Shows the next 6 hidden project cards each click.
   Works with:
   - .project-card.hidden
   - .project-extra
   - .extra-project
   ========================================================= */

function setupIncrementalProjects() {
  const button = document.querySelector("#toggleProjects");

  const extraProjects = Array.from(
    document.querySelectorAll(
      ".project-card.hidden, .project-extra, .extra-project"
    )
  );

  const step = 6;
  let visibleCount = 0;

  if (!button || extraProjects.length === 0) {
    if (button) button.style.display = "none";
    return;
  }

  // Hide all extra projects on page load.
  extraProjects.forEach((card) => {
    card.style.display = "none";
    card.classList.remove("visible-extra");
  });

  button.textContent = "Show More Projects ↓";
  button.setAttribute("aria-expanded", "false");

  button.addEventListener("click", () => {
    const allVisible = visibleCount >= extraProjects.length;

    // Collapse back to first 6 visible projects.
    if (allVisible) {
      visibleCount = 0;

      extraProjects.forEach((card) => {
        card.style.display = "none";
        card.classList.remove("visible-extra");
      });

      button.textContent = "Show More Projects ↓";
      button.setAttribute("aria-expanded", "false");
      return;
    }

    // Show next 6.
    visibleCount = Math.min(visibleCount + step, extraProjects.length);

    extraProjects.forEach((card, index) => {
      const shouldShow = index < visibleCount;
      card.style.display = shouldShow ? "flex" : "none";
      card.classList.toggle("visible-extra", shouldShow);
    });

    button.textContent =
      visibleCount >= extraProjects.length
        ? "Show Fewer Projects ↑"
        : "Show More Projects ↓";

    button.setAttribute("aria-expanded", "true");
  });
}

/* =========================================================
   MAP SHOWCASE
   Fixes map thumbnail buttons.
   Works with:
   - .map-thumb
   - .map-thumb-button
   ========================================================= */

function setupMapShowcase() {
  const maps = [
    {
      title: "Heathrow's Global Reach",
      cat: "Flowline Cartography",
      text: "A global aviation flow map showing Heathrow's international connections using a dark basemap, curved flowlines, and strong visual hierarchy.",
      focus: "Flowlines, global connections, visual hierarchy",
      tools: "ArcGIS Pro, cartographic design",
      img: "assets/images/maps/previews/heathrow-global-reach.jpg",
      story: "maps/heathrow-global-reach.html",
      alt: "Heathrow global reach flowline map preview"
    },
    {
      title: "Calgary Park Accessibility and Social Deprivation",
      cat: "Urban GIS / Accessibility",
      text: "An urban GIS map exploring park accessibility and social deprivation patterns in Calgary, designed for planning and equity-focused interpretation.",
      focus: "Accessibility, social deprivation, urban planning",
      tools: "ArcGIS Pro, spatial analysis",
      img: "assets/images/maps/previews/calgary-park-accessibility.jpg",
      story: "maps/calgary-park-accessibility.html",
      alt: "Calgary park accessibility map preview"
    },
    {
      title: "Housing Cost in Calgary: DA vs CT",
      cat: "Urban GIS / Census Mapping",
      text: "A census-based comparison map showing housing costs at dissemination area and census tract scales, useful for explaining spatial aggregation and scale effects.",
      focus: "Housing cost, census geography, DA vs CT comparison",
      tools: "ArcGIS Pro, census mapping",
      img: "assets/images/maps/previews/housing-cost-da-vs-ct.png",
      story: "maps/housing-cost-da-vs-ct.html",
      alt: "Housing cost map comparing dissemination areas and census tracts"
    },
    {
      title: "Paradise Valley Trail Run Routes",
      cat: "Terrain / Route Mapping",
      text: "A terrain-focused race route map showing 5K and 10K trail routes with elevation, route context, and supporting map elements.",
      focus: "Route design, terrain, elevation profile",
      tools: "ArcGIS Pro, cartographic layout",
      img: "assets/images/maps/previews/paradise-valley-trail-run.jpg",
      story: "maps/paradise-valley-trail-run.html",
      alt: "Paradise Valley Trail Run route map preview"
    },
    {
      title: "Flood Affected Settlements of Chiniot",
      cat: "Disaster Mapping",
      text: "A flood impact map showing affected settlements, district context, satellite imagery, and supporting location information for disaster mapping.",
      focus: "Flood impact, settlements, satellite imagery",
      tools: "ArcGIS Pro, remote sensing context",
      img: "assets/images/maps/previews/flood-affected-settlements.jpg",
      story: "maps/flood-affected-settlements.html",
      alt: "Flood affected settlements of Chiniot map preview"
    },
    {
      title: "Town of Olds and Surrounding Area",
      cat: "Reference Mapping",
      text: "A traditional reference map showing the Town of Olds and surrounding area with road hierarchy, water features, railway, inset map, and supporting map elements.",
      focus: "Reference mapping, road hierarchy, inset design",
      tools: "ArcGIS Pro, cartographic layout",
      img: "assets/images/maps/previews/town-of-olds-reference-map.jpg",
      story: "maps/town-of-olds-reference-map.html",
      alt: "Town of Olds and surrounding area reference map preview"
    },
    {
      title: "Red Carpet Community Spatial Overview",
      cat: "Urban / Neighbourhood Mapping",
      text: "A local-scale community map showing building types, roads, parks, bus stops, and community boundary with a clean inset and neighbourhood-level layout.",
      focus: "Community mapping, urban features, local context",
      tools: "ArcGIS Pro, urban cartography",
      img: "assets/images/maps/previews/red-carpet-community-overview.jpg",
      story: "maps/red-carpet-community-overview.html",
      alt: "Red Carpet community spatial overview map preview"
    },
    {
      title: "Friends of Greens Street Tree Planting",
      cat: "Environmental / Urban Greening",
      text: "A thematic map combining street tree planting counts with tree canopy coverage by Calgary electoral division to support urban greening interpretation.",
      focus: "Tree planting, canopy cover, environmental mapping",
      tools: "ArcGIS Pro, thematic cartography",
      img: "assets/images/maps/previews/friends-of-greens-tree-canopy.jpg",
      story: "maps/friends-of-greens-tree-canopy.html",
      alt: "Friends of Greens street tree planting and tree canopy map preview"
    },
    {
      title: "Stillbirths and Neonatal Deaths in Asia",
      cat: "Health Geography",
      text: "A health geography map set comparing stillbirths and neonatal deaths in Asia using multiple thematic mapping approaches.",
      focus: "Health outcomes, thematic mapping, Asia",
      tools: "ArcGIS Pro, health geography",
      img: "assets/images/maps/previews/stillbirths-neonatal-deaths-asia.jpg",
      story: "maps/stillbirths-neonatal-deaths-asia.html",
      alt: "Stillbirths and neonatal deaths in Asia map preview"
    },
    {
      title: "Pakistan Rural Household Panel Survey Coverage Map",
      cat: "Research / Survey Mapping",
      text: "A research-support map showing surveyed districts in Pakistan, designed to communicate geographic coverage for a rural household panel survey.",
      focus: "Survey coverage, administrative mapping, Pakistan",
      tools: "ArcGIS Pro, research mapping",
      img: "assets/images/maps/previews/pakistan-prhps-coverage-map.jpg",
      story: "maps/pakistan-prhps-coverage-map.html",
      alt: "Pakistan Rural Household Panel Survey coverage map preview"
    }
  ];

  let currentMapIndex = 0;

  const elements = {
    img: document.querySelector("#mapShowcaseImage"),
    cat: document.querySelector("#mapShowcaseCategory"),
    title: document.querySelector("#mapShowcaseTitle"),
    text: document.querySelector("#mapShowcaseText"),
    focus: document.querySelector("#mapShowcaseFocus"),
    tools: document.querySelector("#mapShowcaseTools"),
    story: document.querySelector("#mapShowcaseStory"),
    prev: document.querySelector("#prevMap"),
    next: document.querySelector("#nextMap"),
    thumbs: document.querySelectorAll(".map-thumb, .map-thumb-button")
  };

  function updateMap(index) {
    const map = maps[index];
    if (!map) return;

    if (elements.img) {
      elements.img.src = map.img;
      elements.img.alt = map.alt;
    }

    if (elements.cat) elements.cat.textContent = map.cat;
    if (elements.title) elements.title.textContent = map.title;
    if (elements.text) elements.text.textContent = map.text;
    if (elements.focus) elements.focus.textContent = map.focus;
    if (elements.tools) elements.tools.textContent = map.tools;
    if (elements.story) elements.story.href = map.story;

    elements.thumbs.forEach((thumb) => {
      thumb.classList.toggle("active", Number(thumb.dataset.mapIndex) === index);
    });

    currentMapIndex = index;
  }

  if (elements.prev) {
    elements.prev.addEventListener("click", () => {
      updateMap((currentMapIndex - 1 + maps.length) % maps.length);
    });
  }

  if (elements.next) {
    elements.next.addEventListener("click", () => {
      updateMap((currentMapIndex + 1) % maps.length);
    });
  }

  elements.thumbs.forEach((thumb) => {
    thumb.addEventListener("click", () => {
      updateMap(Number(thumb.dataset.mapIndex));
    });
  });

  updateMap(0);
}

/* =========================================================
   CERTIFICATES
   Shows the next 6 certificate cards each click.
   Works with:
   - .cert-extra
   - .certificate-extra
   - .cert-item.hidden
   Fallback:
   - if no extra class exists, it treats certificates after the first 6 as hidden.
   ========================================================= */

function setupIncrementalCertificates() {
  const list = document.querySelector("#certificatesList");
  const button = document.querySelector("#showMoreCertificates");

  if (!list || !button) return;

  let extraCertificates = Array.from(
    list.querySelectorAll(".cert-extra, .certificate-extra, .cert-item.hidden")
  );

  // Fallback: if no cert-extra classes exist, hide every certificate after the first 6.
  if (extraCertificates.length === 0) {
    const allCertificates = Array.from(list.querySelectorAll(".cert-item, .certificate-card"));
    extraCertificates = allCertificates.slice(6);
  }

  const step = 6;
  let visibleCount = 0;

  if (extraCertificates.length === 0) {
    button.style.display = "none";
    return;
  }

  // Hide all extra certificates on page load.
  extraCertificates.forEach((card) => {
    card.style.display = "none";
    card.classList.remove("visible-extra");
  });

  button.textContent = "Show more certificates ↓";
  button.setAttribute("aria-expanded", "false");

  button.addEventListener("click", () => {
    const allVisible = visibleCount >= extraCertificates.length;

    // Collapse back to first 6 visible certificates.
    if (allVisible) {
      visibleCount = 0;

      extraCertificates.forEach((card) => {
        card.style.display = "none";
        card.classList.remove("visible-extra");
      });

      button.textContent = "Show more certificates ↓";
      button.setAttribute("aria-expanded", "false");
      button.classList.remove("is-open");
      return;
    }

    // Show next 6.
    visibleCount = Math.min(visibleCount + step, extraCertificates.length);

    extraCertificates.forEach((card, index) => {
      const shouldShow = index < visibleCount;
      card.style.display = shouldShow ? "grid" : "none";
      card.classList.toggle("visible-extra", shouldShow);
    });

    button.textContent =
      visibleCount >= extraCertificates.length
        ? "Show fewer certificates ↑"
        : "Show more certificates ↓";

    button.setAttribute("aria-expanded", "true");
    button.classList.toggle("is-open", visibleCount >= extraCertificates.length);
  });
}