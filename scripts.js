

document.querySelectorAll(".card").forEach(card => {
  const productos = JSON.parse(card.getAttribute("data-productos") || "{}");
  if (!Object.keys(productos).length) return;

  const botones = card.querySelectorAll(".opcion-btn");
  const imagen = card.querySelector("img");
  const skuDisplay = card.querySelector(".sku-display");

  botones.forEach((btn, i) => {
    btn.addEventListener("click", (e) => {
      botones.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const opcion = btn.textContent.trim();
      if (productos[opcion]) {
        if(imagen) imagen.src = productos[opcion].img;
        if(skuDisplay) skuDisplay.textContent = productos[opcion].sku;
      }
    });
  });

  // Inicializar con la opción activa
  const btnActivo = card.querySelector(".opcion-btn.active") || botones[0];
  if (btnActivo) btnActivo.click();
});

document.querySelectorAll(".card").forEach(card => {
  const selector = card.querySelector(".selector-talla");
  if (!selector) return; // Si no hay selector, saltar

  selector.addEventListener("change", () => {
    const skus = JSON.parse(card.getAttribute("data-skus"));
    const skuDisplay = card.querySelector(".sku-display");
    const talla = selector.value;

    if (skus && skuDisplay && talla in skus) {
      skuDisplay.textContent = skus[talla];
    }
  });

  // Opcional: disparar cambio para poner SKU correcto al cargar
  selector.dispatchEvent(new Event("change"));
});