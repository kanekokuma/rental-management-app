document.addEventListener("DOMContentLoaded", () => {
  const table = document.querySelector("[data-equipment-table]");
  if (!table) return;

  const rows = Array.from(table.querySelectorAll("[data-item-row]"));
  const searchInput = document.querySelector("#item-search");
  const categorySelect = document.querySelector("[data-filter-category]");
  const statusSelect = document.querySelector("[data-filter-status]");
  const summary = document.querySelector("[data-list-summary]");
  const emptyMessage = document.querySelector("[data-filter-empty]");

  const normalize = (value) => (value || "").toString().trim().toLowerCase();

  const updateList = () => {
    const keyword = normalize(searchInput?.value);
    const category = normalize(categorySelect?.value);
    const status = normalize(statusSelect?.value);
    let visibleCount = 0;

    rows.forEach((row) => {
      const haystack = normalize(
        [
          row.dataset.name,
          row.dataset.category,
          row.dataset.categoryLabel,
          row.dataset.status,
          row.dataset.statusLabel,
        ].join(" ")
      );

      const matchesKeyword = !keyword || haystack.includes(keyword);
      const matchesCategory = !category || normalize(row.dataset.category) === category;
      const matchesStatus = !status || normalize(row.dataset.status) === status;
      const isVisible = matchesKeyword && matchesCategory && matchesStatus;

      row.hidden = !isVisible;
      row.classList.toggle("is-visible", isVisible);
      if (isVisible) visibleCount += 1;
    });

    if (summary) {
      summary.textContent = `${visibleCount}件 / ${rows.length}件を表示中`;
    }
    if (emptyMessage) {
      emptyMessage.hidden = visibleCount !== 0;
    }
  };

  searchInput?.addEventListener("input", updateList);
  categorySelect?.addEventListener("change", updateList);
  statusSelect?.addEventListener("change", updateList);
  updateList();
});
