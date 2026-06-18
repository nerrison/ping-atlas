async function loadComponent(element, url) {
  const cacheKey = `component:${url}`;

  // Check sessionStorage first
  const cached = sessionStorage.getItem(cacheKey);

  if (cached) {
    element.innerHTML = cached;
    return;
  }

  try {
    const response = await fetch(url, {
      cache: "force-cache"
    });

    const html = await response.text();

    sessionStorage.setItem(cacheKey, html);
    element.innerHTML = html;
  } catch (err) {
    console.error(`Failed to load ${url}`, err);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const components = document.querySelectorAll("[data-include]");

  await Promise.all(
    [...components].map(el =>
      loadComponent(el, el.dataset.include)
    )
  );
});