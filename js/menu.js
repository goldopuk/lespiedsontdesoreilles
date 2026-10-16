// Menu du haut sur téléphone : bouton « Menu » qui déplie la liste des pages.
(function () {
  var btn = document.querySelector(".nav-toggle");
  var header = document.querySelector(".site-header");
  if (!btn || !header) return;
  function set(open) {
    header.classList.toggle("open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { set(btn.getAttribute("aria-expanded") !== "true"); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") set(false); });
  header.querySelectorAll("nav a").forEach(function (a) { a.addEventListener("click", function () { set(false); }); });
})();
