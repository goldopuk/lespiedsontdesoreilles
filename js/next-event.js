// « Prochain rendez-vous » : garde les événements dont la date n'est pas passée (calcul dans le navigateur du visiteur).
document.querySelectorAll(".next-event").forEach(function (box) {
  var events;
  try { events = JSON.parse(box.dataset.events); } catch (e) { return; }
  var now = new Date();
  var today = now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  var next = events.filter(function (e) { return e.d >= today; }).slice(0, 3);
  var list = box.querySelector(".next-list");
  if (!next.length) { box.hidden = true; return; }
  list.textContent = "";
  next.forEach(function (e) {
    var a = document.createElement("a");
    a.href = e.u;
    var t = document.createElement("strong"); t.textContent = e.t;
    var d = document.createElement("span"); d.textContent = e.l;
    a.appendChild(t); a.appendChild(d); list.appendChild(a);
  });
  box.hidden = false;
});
