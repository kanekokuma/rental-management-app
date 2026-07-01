document.addEventListener("DOMContentLoaded", () => {
  const table = document.querySelector("[data-equipment-table]");
  if (!table) return;

  const rows = Array.from(table.querySelectorAll("[data-item-row]"));
  const searchInput = document.querySelector("#item-search");
  const categorySelect = document.querySelector("[data-filter-category]");
  const statusSelect = document.querySelector("[data-filter-status]");
  const summary = document.querySelector("[data-list-summary]");
  const emptyMessage = document.querySelector("[data-filter-empty]");
  const clearButton = document.querySelector("[data-clear-filters]");

  // let the "ledger" summary line announce changes to screen readers
  if (summary && !summary.hasAttribute("aria-live")) {
    summary.setAttribute("aria-live", "polite");
  }

  const normalize = (value) => (value || "").toString().trim().toLowerCase();

  // debounce helper so filtering doesn't run on every single keystroke
  const debounce = (fn, wait = 120) => {
    let timer;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), wait);
    };
  };

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

      if (isVisible) {
        // stagger the reveal so filtered results settle in like tags
        // being flipped into view, rather than all popping at once
        row.style.setProperty("--i", visibleCount);
        // restart the CSS transition cleanly
        row.classList.remove("is-visible");
        // eslint-disable-next-line no-unused-expressions
        row.offsetHeight; // force reflow so the transition replays
        row.classList.add("is-visible");
        visibleCount += 1;
      } else {
        row.classList.remove("is-visible");
      }
    });

    if (summary) {
      summary.textContent = `${visibleCount}件 / ${rows.length}件を表示中`;
    }

    if (emptyMessage) {
      emptyMessage.hidden = visibleCount !== 0;
    }

    if (clearButton) {
      const hasActiveFilter = Boolean(keyword || category || status);
      clearButton.hidden = !hasActiveFilter;
    }
  };

  const debouncedUpdate = debounce(updateList, 120);

  searchInput?.addEventListener("input", debouncedUpdate);
  categorySelect?.addEventListener("change", updateList);
  statusSelect?.addEventListener("change", updateList);

  clearButton?.addEventListener("click", () => {
    if (searchInput) searchInput.value = "";
    if (categorySelect) categorySelect.value = "";
    if (statusSelect) statusSelect.value = "";
    updateList();
    searchInput?.focus();
  });

  // sortable columns: add [data-sort-key] to a <th> to enable click-to-sort
  const sortableHeaders = Array.from(table.querySelectorAll("[data-sort-key]"));
  const tbody = table.querySelector("tbody");
  let currentSort = { key: null, direction: 1 };

  sortableHeaders.forEach((th) => {
    th.setAttribute("role", "button");
    th.setAttribute("tabindex", "0");

    const sortByHeader = () => {
      const key = th.dataset.sortKey;
      const direction = currentSort.key === key ? currentSort.direction * -1 : 1;
      currentSort = { key, direction };

      sortableHeaders.forEach((header) => header.removeAttribute("aria-sort"));
      th.setAttribute("aria-sort", direction === 1 ? "ascending" : "descending");

      const sorted = [...rows].sort((a, b) => {
        const valueA = normalize(a.dataset[key]);
        const valueB = normalize(b.dataset[key]);
        const numA = parseFloat(valueA);
        const numB = parseFloat(valueB);
        const bothNumeric = !Number.isNaN(numA) && !Number.isNaN(numB);
        const comparison = bothNumeric
          ? numA - numB
          : valueA.localeCompare(valueB, "ja");
        return comparison * direction;
      });

      sorted.forEach((row) => tbody.appendChild(row));
      updateList();
    };

    th.addEventListener("click", sortByHeader);
    th.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        sortByHeader();
      }
    });
  });

  // initial staggered reveal on page load
  updateList();
});
