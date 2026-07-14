(() => {
  const menuToggle = document.getElementById("menuToggle");
  const primaryNav = document.getElementById("primaryNav");

  if (menuToggle && primaryNav) {
    const closeMenu = () => {
      primaryNav.classList.remove("is-open");
      menuToggle.setAttribute("aria-expanded", "false");
    };

    menuToggle.addEventListener("click", () => {
      const isOpen = primaryNav.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    primaryNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
  }

  const dialog = document.getElementById("mapDialog");
  const dialogTitle = document.getElementById("mapDialogTitle");
  const dialogImage = document.getElementById("mapDialogImage");
  const mapStage = document.getElementById("mapStage");
  const mapHelp = document.getElementById("mapHelp");
  const zoomOut = document.getElementById("zoomOut");
  const zoomReset = document.getElementById("zoomReset");
  const zoomIn = document.getElementById("zoomIn");
  const mapClose = document.getElementById("mapClose");

  if (dialog && dialogTitle && dialogImage && mapStage && mapHelp && zoomOut && zoomReset && zoomIn && mapClose) {
    let scale = 1;
    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;
    let dragStartX = 0;
    let dragStartY = 0;

    const renderMap = () => {
      dialogImage.style.transform = `translate(${offsetX}px, ${offsetY}px) scale(${scale})`;
      const percent = Math.round(scale * 100);
      zoomReset.textContent = `${percent}%`;
      zoomOut.disabled = scale <= 1;
      zoomIn.disabled = scale >= 5;
      mapHelp.textContent = `${percent}% · Use + and − to zoom. Drag the map when enlarged.`;
    };

    const resetMap = () => {
      scale = 1;
      offsetX = 0;
      offsetY = 0;
      renderMap();
    };

    const setScale = (nextScale) => {
      scale = Math.min(5, Math.max(1, nextScale));
      if (scale === 1) {
        offsetX = 0;
        offsetY = 0;
      }
      renderMap();
    };

    document.querySelectorAll(".map-trigger").forEach((trigger) => {
      trigger.addEventListener("click", (event) => {
        event.preventDefault();
        dialogTitle.textContent = trigger.dataset.title || "Map";
        dialogImage.alt = trigger.dataset.alt || "Full map";
        mapHelp.textContent = "Loading full-resolution map…";
        resetMap();
        dialogImage.src = trigger.dataset.full || trigger.href;
        document.body.classList.add("dialog-open");
        dialog.showModal();
      });
    });

    dialogImage.addEventListener("load", renderMap);
    mapClose.addEventListener("click", () => dialog.close());
    zoomIn.addEventListener("click", () => setScale(scale + 0.5));
    zoomOut.addEventListener("click", () => setScale(scale - 0.5));
    zoomReset.addEventListener("click", resetMap);

    mapStage.addEventListener("wheel", (event) => {
      event.preventDefault();
      setScale(scale + (event.deltaY < 0 ? 0.25 : -0.25));
    }, { passive: false });

    mapStage.addEventListener("pointerdown", (event) => {
      if (scale === 1) return;
      isDragging = true;
      dragStartX = event.clientX - offsetX;
      dragStartY = event.clientY - offsetY;
      mapStage.classList.add("is-dragging");
      mapStage.setPointerCapture(event.pointerId);
    });

    mapStage.addEventListener("pointermove", (event) => {
      if (!isDragging) return;
      offsetX = event.clientX - dragStartX;
      offsetY = event.clientY - dragStartY;
      renderMap();
    });

    const stopDragging = (event) => {
      if (!isDragging) return;
      isDragging = false;
      mapStage.classList.remove("is-dragging");
      if (mapStage.hasPointerCapture(event.pointerId)) {
        mapStage.releasePointerCapture(event.pointerId);
      }
    };

    mapStage.addEventListener("pointerup", stopDragging);
    mapStage.addEventListener("pointercancel", stopDragging);

    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", () => {
      document.body.classList.remove("dialog-open");
      resetMap();
    });

    renderMap();
  }

  const track = document.getElementById("photoTrack");
  const previousButton = document.getElementById("carouselPrev");
  const nextButton = document.getElementById("carouselNext");
  const currentLabel = document.getElementById("carouselCurrent");
  const totalLabel = document.getElementById("carouselTotal");

  if (track && previousButton && nextButton && currentLabel && totalLabel) {
    const slides = Array.from(track.querySelectorAll(".photo-slide"));
    totalLabel.textContent = String(slides.length);

    const getStep = () => {
      const firstSlide = slides[0];
      if (!firstSlide) return track.clientWidth;
      const styles = window.getComputedStyle(track);
      const gap = Number.parseFloat(styles.columnGap || styles.gap) || 0;
      return firstSlide.getBoundingClientRect().width + gap;
    };

    const updateCarousel = () => {
      const step = getStep();
      const current = Math.min(slides.length, Math.max(1, Math.round(track.scrollLeft / step) + 1));
      currentLabel.textContent = String(current);
      previousButton.disabled = track.scrollLeft <= 2;
      nextButton.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    };

    previousButton.addEventListener("click", () => {
      track.scrollBy({ left: -getStep(), behavior: "smooth" });
    });

    nextButton.addEventListener("click", () => {
      track.scrollBy({ left: getStep(), behavior: "smooth" });
    });

    let scrollFrame = 0;
    track.addEventListener("scroll", () => {
      window.cancelAnimationFrame(scrollFrame);
      scrollFrame = window.requestAnimationFrame(updateCarousel);
    }, { passive: true });

    track.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        track.scrollBy({ left: -getStep(), behavior: "smooth" });
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        track.scrollBy({ left: getStep(), behavior: "smooth" });
      }
    });

    window.addEventListener("resize", updateCarousel);
    updateCarousel();
  }
})();
