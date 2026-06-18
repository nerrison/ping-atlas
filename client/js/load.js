document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".search");
    const tableBody = document.getElementById("resourceTableBody");

    let timer;

    loadData("");

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            clearTimeout(timer);

            timer = setTimeout(() => {
                loadData(e.target.value.trim());
            }, 300);
        });
    }

    function formatStatus(status) {
        if (status === "up") return "UP";
        if (status === "degraded") return "DEGRADED";
        if (status === "down") return "DOWN";
        return "Undefined";
    }

    async function loadData(query = "") {
        try {
            const [groupsRes, endpointsRes] = await Promise.all([
                fetch("/client/data/groups.json"),
                fetch("/client/data/endpoints.json")
            ]);

            const groups = await groupsRes.json();
            const endpoints = await endpointsRes.json();

            const groupById = Object.fromEntries(
                groups.map(g => [g.id, g])
            );

            let results = [];
            const q = query.toLowerCase();

            if (!q) {
                results = groups.map(g => ({
                    ...g,
                    type: "group"
                }));
            } else {
                const groupMatches = groups
                    .filter(g =>
                        g.name.toLowerCase().includes(q) ||
                        g.description.toLowerCase().includes(q) ||
                        g.baseUrl.toLowerCase().includes(q)
                    )
                    .map(g => ({ ...g, type: "group" }));

                const endpointMatches = endpoints
                    .filter(e =>
                        e.url.toLowerCase().includes(q) ||
                        e.description.toLowerCase().includes(q)
                    )
                    .map(e => ({ ...e, type: "endpoint" }));

                results = [...groupMatches, ...endpointMatches];
            }

            tableBody.innerHTML = results.map(item => {
                let href = "#";

                if (item.type === "group") {
                    href = `group.html?slug=${encodeURIComponent(item.slug)}`;
                }

                if (item.type === "endpoint") {
                    const group = groupById[item.groupId];
                    const groupSlug = group ? group.slug : "unknown";

                    href = `endpoint.html?slug=${encodeURIComponent(groupSlug)}&id=${encodeURIComponent(item.id)}`;
                }

                return `
                    <tr class="border-b hover:bg-gray-100 transition cursor-pointer"
                        onclick="window.location.href='${href}'">

                        <td class="p-3">${formatStatus(item.status)}</td>

                        <td class="p-3 font-medium">
                            ${item.type === "endpoint" ? item.url : item.name}
                        </td>

                        <td class="p-3 capitalize">${item.type}</td>

                        <td class="p-3">${item.description || "N/A"}</td>

                        <td class="p-3">
                            ${item.response ? item.response + "ms" : "-"}
                        </td>

                        <td class="p-3">
                            ${item.lastCheck || item.lastcheck || "-"}s
                        </td>

                        <td class="p-3">
                            ${item.uptime || "0"}%
                        </td>

                    </tr>
                `;
            }).join("");

        } catch (err) {
            console.error("Load error:", err);

            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="p-4 text-center">
                        Failed to load data
                    </td>
                </tr>
            `;
        }
    }
});