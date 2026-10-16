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
