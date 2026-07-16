// SAVANT PHOTO GALLERY - MODERN INTEGRATION SCRIPT

// Curated gorgeous high-resolution Unsplash images as fallbacks for local assets
const IMAGE_FALLBACKS = {
    "/assets/images/golden-hour.jpg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "/assets/images/urban-neon.jpg": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=800&q=80",
    "/assets/images/minimalist-shadows.jpg": "https://images.unsplash.com/photo-1500485035595-cbe6f645feb1?auto=format&fit=crop&w=800&q=80",
    "/assets/images/pine-forest.jpg": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
    "/assets/images/brutalist-concrete.jpg": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
    "/assets/images/abstract-curves.jpg": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?auto=format&fit=crop&w=800&q=80"
};

// Global application state
const state = {
    lastEvaluatedAt: null,
    matchedRules: []
};

// Toast notification helper
function showToast(title, body) {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerHTML = `
        <span class="toast-header">${title}</span>
        <span class="toast-body">${body}</span>
    `;
    container.appendChild(toast);

    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.classList.add("removing");
        toast.addEventListener("animationend", () => {
            toast.remove();
        });
    }, 4000);
}

// Function to call the python rule evaluation API
async function evaluateRequest(event, extraParams = {}) {
    const viewportWidth = window.innerWidth;
    
    try {
        const response = await fetch("/api/evaluate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                event: event,
                viewport_width: viewportWidth,
                ...extraParams
            })
        });

        if (!response.ok) {
            throw new Error(`API returned error code ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Rule engine evaluation failed:", error);
        return null;
    }
}

// Update diagnostic panel with rule evaluation metadata
function updateDiagnostics(event, decision) {
    if (!decision) return;

    const matchedRulesContainer = document.getElementById("matched-rules");
    const lastEventElement = document.getElementById("last-event");
    const evalTimeElement = document.getElementById("eval-time");

    // Format local time nicely
    const now = new Date();
    const timeString = now.toTimeString().split(" ")[0];
    evalTimeElement.textContent = timeString;
    lastEventElement.textContent = `${event} (${window.innerWidth}px)`;

    // Render rule badges
    matchedRulesContainer.innerHTML = "";
    decision.rule_ids.forEach(ruleId => {
        const badge = document.createElement("span");
        badge.className = "rule-badge";
        badge.textContent = ruleId;
        matchedRulesContainer.appendChild(badge);
    });

    // Fire toast if rules matched
    if (JSON.stringify(state.matchedRules) !== JSON.stringify(decision.rule_ids)) {
        state.matchedRules = decision.rule_ids;
        showToast("Rule Engine Evaluated", `Triggered rules: ${decision.rule_ids.join(", ")}`);
    }
}

// Render photo grid to the DOM
function renderPhotos(photos) {
    const grid = document.getElementById("photo-grid");
    grid.innerHTML = "";

    if (!photos || photos.length === 0) {
        grid.innerHTML = '<p class="error-msg">No photos loaded from the Rule Engine.</p>';
        return;
    }

    photos.forEach(photo => {
        // Map asset URLs to beautiful high-resolution unsplash images
        const imageUrl = IMAGE_FALLBACKS[photo.image_url] || photo.image_url;

        const card = document.createElement("article");
        card.className = "photo-card";
        card.dataset.id = photo.id;
        card.innerHTML = `
            <div class="card-image-wrapper">
                <span class="card-badge">${photo.category}</span>
                <img src="${imageUrl}" alt="${photo.title}" class="card-image" loading="lazy">
            </div>
            <div class="card-content">
                <div class="card-info">
                    <h4>${photo.title}</h4>
                    <span class="card-category">Category: ${photo.category}</span>
                </div>
                <div class="card-actions">
                    <button class="action-btn like-btn" aria-label="Like photo">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                        </svg>
                        <span class="likes-count">${photo.likes} Likes</span>
                    </button>
                    <span class="action-btn info-tag">Details</span>
                </div>
            </div>
        `;

        // Wire up R3 Hover Zoom Tracking Interaction
        card.addEventListener("mouseenter", async () => {
            // Ask rule engine to evaluate hover event for R3 zoom trigger
            const decision = await evaluateRequest("hover_photo", { photo_id: photo.id });
            if (decision) {
                updateDiagnostics("hover_photo", decision);
            }
        });

        // Wire up US2 Click / Lightbox Event Interaction
        card.addEventListener("click", async (e) => {
            if (e.target.closest(".like-btn")) {
                e.stopPropagation();
                return;
            }

            const decision = await evaluateRequest("click_photo", { photo_id: photo.id });
            if (decision && decision.outcome === "OPEN_LIGHTBOX") {
                openLightbox(decision.photos[0], decision);
            }
        });

        grid.appendChild(card);
    });
}

// Open Lightbox view [US2]
function openLightbox(photo, decision) {
    const lightbox = document.getElementById("lightbox-overlay");
    const img = document.getElementById("lightbox-img");
    const category = document.getElementById("lightbox-category");
    const title = document.getElementById("lightbox-title");

    const imageUrl = IMAGE_FALLBACKS[photo.image_url] || photo.image_url;
    img.src = imageUrl;
    img.alt = photo.title;
    category.textContent = photo.category;
    title.textContent = photo.title;

    lightbox.classList.add("active");
    lightbox.setAttribute("aria-hidden", "false");
    
    updateDiagnostics("click_photo", decision);
}

// Close Lightbox view [US2]
function closeLightbox() {
    const lightbox = document.getElementById("lightbox-overlay");
    lightbox.classList.remove("active");
    lightbox.setAttribute("aria-hidden", "true");
}

// Bind Lightbox Close Interactions [US2]
function bindLightboxEvents() {
    const lightbox = document.getElementById("lightbox-overlay");
    const closeBtn = document.getElementById("lightbox-close-btn");

    closeBtn.addEventListener("click", closeLightbox);
    
    // Close on background overlay click
    lightbox.addEventListener("click", (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Close on Escape key press
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && lightbox.classList.contains("active")) {
            closeLightbox();
        }
    });
}

// Initial application load
async function initGallery() {
    // Bind click/close handlers
    bindLightboxEvents();

    // Evaluate gallery load request with current viewport size
    const decision = await evaluateRequest("load_gallery");
    if (decision) {
        renderPhotos(decision.photos);
        updateDiagnostics("load_gallery", decision);
    }
}

// Re-evaluate on window resize (to trigger mobile R2 grid collapse live!)
let resizeTimeout;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(async () => {
        const decision = await evaluateRequest("load_gallery");
        if (decision) {
            updateDiagnostics("load_gallery", decision);
        }
    }, 150);
});

// Run app
document.addEventListener("DOMContentLoaded", initGallery);

