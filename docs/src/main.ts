const root: HTMLElement = document.documentElement;
const headers: NodeListOf<HTMLElement> = document.querySelectorAll<HTMLElement>(".doc-header");
const toggleBtn: HTMLElement | null = document.getElementById("theme-toggle");
const saved: string | null = localStorage.getItem("docs-theme");
const prefersDark: boolean = window.matchMedia("(prefers-color-scheme: dark)").matches;


headers.forEach((header: HTMLElement) => {
    header.addEventListener("click", (event: MouseEvent) => {
        event.stopPropagation();
        const parentItem = header.closest<HTMLElement>(".doc-item");
        parentItem?.classList.toggle("open");
    });
});

function applyTheme(theme: string): void {
    if (!toggleBtn) return;

    if (theme === "dark") {
        root.setAttribute("data-theme", "dark");
        toggleBtn.textContent = "☀️";
    } else {
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
