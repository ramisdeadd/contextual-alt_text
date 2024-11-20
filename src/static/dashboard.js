function searchTable() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) { 
      const cells = rows[i].getElementsByTagName('td');
      let match = false;

      for (let j = 0; j < cells.length; j++) {
        cells[j].innerHTML = cells[j].innerText;

        const text = cells[j].innerText;
        const lowerText = text.toLowerCase();
        if (lowerText.includes(filter) && filter !== '') {
          const regex = new RegExp(`(${filter})`, 'gi');
          cells[j].innerHTML = text.replace(regex, '<span class="highlight-dashboard">$1</span>');
          match = true;
        }
      }

      rows[i].style.display = match ? '' : 'none';
    }
  }