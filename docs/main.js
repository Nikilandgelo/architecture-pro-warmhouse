/* jshint esversion: 6 */

(function () {
    "use strict";

    const items = document.querySelectorAll(".doc-item");

    items.forEach((item) => {
        item.querySelector(".doc-header").addEventListener("click", () => {
            item.classList.toggle("open");
        });
    });

    const toggleBtn = document.getElementById("theme-toggle");
    const root = document.documentElement;

    function applyTheme(theme) {
        if (theme === "dark") {
            root.setAttribute("data-theme", "dark");
            toggleBtn.textContent = "☀️";
        } else {
            root.removeAttribute("data-theme");
            toggleBtn.textContent = "🌙";
        }

        localStorage.setItem("docs-theme", theme);
    }

    const saved = localStorage.getItem("docs-theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    applyTheme(saved || (prefersDark ? "dark" : "light"));

    toggleBtn.addEventListener("click", () => {
        const isDark = root.getAttribute("data-theme") === "dark";
        applyTheme(isDark ? "light" : "dark");
    });
}());
