// LPJ-EOSIM ecosystem page: load the interactive figure into #ecosystem-figure, then give every tile a
// mouse-following 3D tilt. Tiles (a.eco-link > g.eco-tile) are copied into HTML cards laid over the figure,
// because CSS 3D transforms don't render on elements inside an SVG. Tiles only tilt; they don't link anywhere.
(async () => {
  const host = document.getElementById("ecosystem-figure");
  if (!host) return;
  const response = await fetch(host.dataset.src);
  if (!response.ok) return; // the <noscript> image stays the fallback
  host.innerHTML = await response.text();
  const svg = host.querySelector("svg");

  const maxTilt = 16; // degrees at the card edge
  const pad = 1.5; // viewBox units around each tile, so its stroke isn't clipped
  const svgNS = "http://www.w3.org/2000/svg";
  const view = svg.viewBox.baseVal;
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const wrap = document.createElement("div");
  wrap.className = "eco-wrap";
  svg.parentNode.insertBefore(wrap, svg);
  wrap.appendChild(svg);
  const stage = document.createElement("div");
  stage.className = "eco-stage";
  wrap.appendChild(stage);

  for (const link of svg.querySelectorAll("a.eco-link")) {
    const tile = link.querySelector(".eco-tile");
    const box = tile.getBBox();
    const x = box.x - pad, y = box.y - pad, w = box.width + 2 * pad, h = box.height + 2 * pad;

    const card = document.createElement("div");
    card.className = "eco-card";
    card.style.left = `${((x - view.x) / view.width) * 100}%`;
    card.style.top = `${((y - view.y) / view.height) * 100}%`;
    card.style.width = `${(w / view.width) * 100}%`;
    card.style.height = `${(h / view.height) * 100}%`;

    const mini = document.createElementNS(svgNS, "svg");
    mini.setAttribute("viewBox", `${x} ${y} ${w} ${h}`);
    mini.setAttribute("font-family", svg.getAttribute("font-family"));
    const copy = tile.cloneNode(true);
    copy.removeAttribute("id");
    copy.querySelectorAll("[id]").forEach((el) => el.removeAttribute("id"));
    mini.appendChild(copy);

    const glare = document.createElement("span");
    glare.className = "eco-glare";
    card.append(mini, glare);
    stage.appendChild(card);

    tile.style.visibility = "hidden"; // the card draws it now
    link.removeAttribute("href"); // no per-tile sections on this page, so the tile isn't a link

    if (still) continue;
    card.addEventListener("pointermove", (event) => {
      const r = card.getBoundingClientRect();
      const px = (event.clientX - r.left) / r.width - 0.5;
      const py = (event.clientY - r.top) / r.height - 0.5;
      card.style.transform = `perspective(700px) rotateX(${-py * maxTilt}deg) rotateY(${px * maxTilt}deg) scale(1.035)`;
      card.style.setProperty("--gx", `${(px + 0.5) * 100}%`);
      card.style.setProperty("--gy", `${(py + 0.5) * 100}%`);
    });
    card.addEventListener("pointerleave", () => {
      card.style.transform = "";
    });
  }
})();
