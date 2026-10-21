// Lecteur YouTube « au clic » : l'iframe (et donc YouTube) n'est chargée qu'après un clic du visiteur.
document.addEventListener("click", function (e) {
  var b = e.target.closest(".video-lite");
  if (!b) return;
  var f = document.createElement("iframe");
  f.src = "https://www.youtube-nocookie.com/embed/" + b.dataset.id + "?autoplay=1&rel=0";
  f.title = b.dataset.title || "Vidéo";
  f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
  f.allowFullscreen = true;
  f.className = "video-frame";
  b.replaceWith(f);
});

// Page « Vidéos » : recherche (sans tenir compte des accents) et filtre par année
(function () {
  var input = document.getElementById("video-search");
  if (!input) return;
  var cards = Array.prototype.slice.call(document.querySelectorAll(".video-gallery .video"));
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var count = document.getElementById("video-count");
  var none = document.getElementById("video-none");
  var year = "";
  function norm(t) { return t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function apply() {
    var words = norm(input.value).split(/\s+/).filter(Boolean), shown = 0;
    cards.forEach(function (c) {
      var ok = (!year || c.dataset.year === year) && words.every(function (w) { return c.dataset.search.indexOf(w) !== -1; });
      c.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown + " vidéo" + (shown > 1 ? "s" : "") + " affichée" + (shown > 1 ? "s" : "");
    none.hidden = shown > 0;
  }
  input.addEventListener("input", apply);
  chips.forEach(function (b) {
    b.addEventListener("click", function () {
      year = b.dataset.year;
      chips.forEach(function (x) { x.classList.toggle("active", x === b); });
      apply();
    });
  });
  apply();
})();

// Page « Actualités » : champ de recherche (sans tenir compte des accents), les années sans résultat sont masquées
(function () {
  var input = document.getElementById("news-search");
  if (!input) return;
  var cards = Array.prototype.slice.call(document.querySelectorAll(".news-year .news-card"));
  var years = Array.prototype.slice.call(document.querySelectorAll(".news-year"));
  var count = document.getElementById("news-count");
  var none = document.getElementById("news-none");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".video-tools .chip"));
  var year = "";
  function norm(t) { return t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function apply() {
    var words = norm(input.value).split(/\s+/).filter(Boolean), shown = 0;
    cards.forEach(function (c) {
      var ok = (!year || c.closest(".news-year").dataset.year === year) && words.every(function (w) { return c.dataset.search.indexOf(w) !== -1; });
      c.hidden = !ok;
      if (ok) shown++;
    });
    years.forEach(function (y) { y.hidden = !y.querySelector(".news-card:not([hidden])"); });
    count.textContent = words.length || year ? shown + " actualité" + (shown > 1 ? "s" : "") + " affichée" + (shown > 1 ? "s" : "") : "";
    none.hidden = shown > 0;
  }
  input.addEventListener("input", apply);
  chips.forEach(function (b) {
    b.addEventListener("click", function () {
      year = b.dataset.year;
      chips.forEach(function (x) { x.classList.toggle("active", x === b); });
      apply();
    });
  });
})();
