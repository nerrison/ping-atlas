document.addEventListener('DOMContentLoaded', () => {
    loadendpoint();
});

async function loadendpoint() {
    const params = new URLSearchParams(window.location.search);

    const slug = params.get('slug');
    const endpointId = Number(params.get('id'));

    if (!slug || !endpointId) return;

    const groups = await (await fetch('/client/data/groups.json')).json();
    const group = groups.find(g => g.slug === slug);
    if (!group) return;
    
    const endpoints = await (await fetch('/client/data/endpoints.json')).json();

    const endpoint = endpoints.find(
        e => e.id === endpointId &&
             e.groupId === group.id
    );

    if (!endpoint) return;

    const set = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
    };

    set('endpointurl', endpoint.url);
    set('description', endpoint.description);
    set('status', endpoint.status);
    set('type', endpoint.type);
    set('method', endpoint.method);
    set('uptime', `${endpoint.uptime}%`);
    set('lastcheck', `${endpoint.lastcheck}s ago`);

    // chart
    initChart(endpoint.history);

    // Breadcrumb
    document.getElementById('breadcrumb').innerHTML = `
        <a href="index.html" class="text-blue-600 hover:underline">Home</a> /
        <a href="group.html?slug=${encodeURIComponent(slug)}" class="text-blue-600 hover:underline">${slug}</a> /
        <span>${endpoint.type}</span>
    `;

    
}