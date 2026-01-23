document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    const clearButton = document.querySelector('.clear-search');
    const searchButton = document.querySelector('.search-button');

    // Clear search input
    clearButton?.addEventListener('click', function() {
        searchInput.value = '';
        searchInput.focus();
        clearButton.style.display = 'none';
    });

    // Handle form submission
    searchForm?.addEventListener('submit', function(e) {
        if (!searchInput.value.trim()) {
            e.preventDefault();
            return;
        }

        searchButton.classList.add('loading');
    });

    // Handle input changes
    searchInput?.addEventListener('input', function() {
        clearButton.style.display = this.value ? 'flex' : 'none';
    });
});
