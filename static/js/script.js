// =========================
// Dark Mode
// =========================

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }

}

// Load saved theme

window.addEventListener("load", () => {

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }

});

// =========================
// Skill Search
// =========================

document.addEventListener("DOMContentLoaded", function () {

    const search = document.getElementById("searchSkill");

    if (search) {

        search.addEventListener("keyup", function () {

            const value = this.value.toLowerCase();

            const rows = document.querySelectorAll("tbody tr");

            rows.forEach(function (row) {

                row.style.display =
                    row.innerText.toLowerCase().includes(value)
                        ? ""
                        : "none";

            });

        });

    }

});

// =========================
// Auto-hide Alerts
// =========================

setTimeout(() => {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        alert.style.transition = "0.5s";

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    });

}, 3000);

// =========================
// Scroll To Top Button
// =========================

window.onscroll = function () {

    const btn = document.getElementById("topBtn");

    if (!btn) return;

    if (document.documentElement.scrollTop > 250) {

        btn.style.display = "block";

    } else {

        btn.style.display = "none";

    }

};

function topFunction() {

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

}

// =========================
// Safe Chart Check
// =========================

if (typeof Chart !== "undefined") {

    console.log("Chart.js Loaded Successfully");

}