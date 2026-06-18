document.addEventListener('DOMContentLoaded', () => {
    loadgroup();
});

async function loadgroup() {
    const params = new URLSearchParams(window.location.search);
    const slugParam = params.get('slug');

    if (!slugParam) return;

    const response = await fetch('/client/data/groups.json');
    const groups = await response.json();

    const group = groups.find(g => g.slug === slugParam);
    if (!group) return;

    document.getElementById('groupname').textContent = group.name;
    document.getElementById('description').textContent = group.description;
    document.getElementById('baseUrl').textContent = group.baseUrl;
    document.getElementById('uptime').textContent = `${group.uptime}%`;
    document.getElementById('response').textContent = `${group.response}ms`;
    document.getElementById('breadcrumb').innerHTML = `
        <a href="index.html" class="text-blue-600 hover:underline">Home</a> /
        <span>${group.name}</span>
    `;

    const endpoints = await(await fetch("/client/data/endpoints.json")).json();

    const groupEndpoints = endpoints.filter(
        ep=>ep.groupId === group.id
    );

    document.getElementById('endpoints').innerHTML =
    groupEndpoints.map(e => {
        return `
            <tr
                class="border-b hover:bg-gray-50 transition cursor-pointer"
                onclick="window.location.href='endpoint.html?slug=${encodeURIComponent(group.slug)}&id=${encodeURIComponent(e.id)}'"
            >
                <td class="px-4 py-3 font-bold">
                    ${e.status?.toUpperCase() || 'N/A'}
                </td>
                <td class="px-4 py-3 font-bold text-blue-800">
                    ${e.url || 'N/A'}
                </td>
                <td class="px-4 py-3 font-bold">
                    ${e.type || 'N/A'}
                </td>
                <td class="px-4 py-3">
                    ${e.method || "N/A"}
                </td>
                <td class="px-4 py-3">
                    ${e.uptime || 0}%
                </td>
                <td class="px-4 py-3">
                    ${e.lastcheck || 0}s
                </td>
                <td class="px-4 py-3">
                    ${e.description || 'N/A'}
                </td>
            </tr>
        `;
    }).join('');
}
