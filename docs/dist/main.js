"use strict";
const root = document.documentElement;
const items = document.querySelectorAll(".doc-item");
const toggleBtn = document.getElementById("theme-toggle");
const saved = localStorage.getItem("docs-theme");
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
items.forEach((item) => {
    const header = item.querySelector(".doc-header");
    header?.addEventListener("click", () => {
        item.classList.toggle("open");
    });
});
function applyTheme(theme) {
    if (!toggleBtn)
        return;
    if (theme === "dark") {
        root.setAttribute("data-theme", "dark");
        toggleBtn.textContent = "☀️";
    }
    else {
        root.removeAttribute("data-theme");
        toggleBtn.textContent = "🌙";
    }
    localStorage.setItem("docs-theme", theme);
}
applyTheme(saved || (prefersDark ? "dark" : "light"));
toggleBtn?.addEventListener("click", () => {
    const isDark = root.getAttribute("data-theme") === "dark";
    applyTheme(isDark ? "light" : "dark");
});
