const wasteGuide = {
    banana: {
        category: "Biodegradable Waste",
        bin: "Wet Waste",
        tip: "Place in the designated wet-waste bin or compost it if suitable."
    },

    food: {
        category: "Biodegradable Waste",
        bin: "Wet Waste",
        tip: "Separate food scraps for composting or your local wet-waste collection."
    },

    plastic: {
        category: "Potentially Recyclable Plastic",
        bin: "Dry Waste Collection",
        tip: "Empty and rinse the bottle. Check local recycling rules."
    },

    paper: {
        category: "Recyclable Paper",
        bin: "Dry Waste Collection",
        tip: "Keep paper clean and dry. Greasy or food-soiled paper may not be recyclable."
    },

    glass: {
        category: "Recyclable Glass",
        bin: "Separate Glass Collection",
        tip: "Use designated glass collection. Handle broken glass carefully."
    },

    battery: {
        category: "Hazardous Household Waste",
        bin: "Authorized Battery Collection",
        tip: "Never place batteries in ordinary wet or dry waste. Use an authorized collection point."
    },

    metal: {
        category: "Potentially Recyclable Metal",
        bin: "Dry Waste Collection",
        tip: "Empty the can and follow your local recycling requirements."
    },

    ewaste: {
        category: "Electronic Waste (E-Waste)",
        bin: "Authorized E-Waste Collection",
        tip: "Do not put old phones in household bins. Use an authorized e-waste collection centre."
    }
};


    async function sortWaste() {
    const search = document.getElementById("wasteSearch");
    const select = document.getElementById("wasteItem");
    const result = document.getElementById("result");

    const item = search.value.trim() || select.value;

    if (!item) {
        result.innerHTML = `
            <p>⚠️ Please enter or select a waste item.</p>
        `;
        return;
    }

    result.innerHTML = "<p>🌱 Analysing waste item...</p>";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ item: item })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to classify this item.");
        }

        result.innerHTML = `
            <h3>🌿 ${data.category}</h3>
            <p><strong>Disposal method:</strong> ${data.method}</p>
            <p><strong>Guidance:</strong> ${data.tip}</p>
            <p><small>Model confidence: ${data.confidence}% — this is not a guarantee of correctness.</small></p>
        `;
    } catch (error) {
        result.innerHTML = `
            <p>⚠️ Could not connect to the ML model.</p>
            <p>Make sure Sortify is running through the Flask server.</p>
        `;
        console.error(error);
    }
}
    //store session statistics
document.getElementById("sortedCount").textContent =
    sessionStorage.getItem("sortedCount") || 0;

document.getElementById("categoryCount").textContent =
    Object.keys(wasteGuide).length;

document.getElementById("tipCount").textContent =
    document.querySelectorAll(".card").length;
    // Daily Eco Challenge
const ecoActions = document.querySelectorAll(".eco-action");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

function updateProgress() {
    const completed = document.querySelectorAll(
        ".eco-action:checked"
    ).length;

    const total = ecoActions.length;
    const percentage = (completed / total) * 100;

    progressBar.style.width = percentage + "%";

    progressText.textContent =
        `${completed} of ${total} challenges completed`;

    document.getElementById("actionCount").textContent = completed;
}

ecoActions.forEach(action => {
    action.addEventListener("change", updateProgress);
});

updateProgress();
// Search for waste items
const wasteSearch = document.getElementById("wasteSearch");
const wasteSelect = document.getElementById("wasteItem");

wasteSearch.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();

    const options = Array.from(wasteSelect.options);

    const match = options.find(option =>
        option.textContent.toLowerCase().includes(query) &&
        option.value !== ""
    );

    if (match && query !== "") {
        wasteSelect.value = match.value;
    }
});