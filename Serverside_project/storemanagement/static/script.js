// JavaScript function to filter products by name
document.getElementById('productFilter').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const rows = document.querySelectorAll('#productTable tbody tr');

    rows.forEach(row => {
        const title = row.querySelector('td a').textContent.toLowerCase();
        if (title.includes(filter)) {
            row.style.display = ''; // Show row
        } else {
            row.style.display = 'none'; // Hide row
        }
    });
});
