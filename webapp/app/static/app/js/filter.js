
  document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.filter-form');
    const nameFilterInput = document.getElementById('title-input');
    const specialtyFilterInput = document.getElementById('specialty-input');
    const tableRows = document.querySelectorAll('.journal-table tbody tr');
    const checkboxes = document.querySelectorAll('.filter-checkbox');

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      applyFilters();
    });
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener('change', function() {
        applyFilters();
      });
    });

    function applyFilters() {
      const nameFilterValue = nameFilterInput.value.toLowerCase();
      const specialtyFilterValue = specialtyFilterInput.value.toLowerCase();
      const selectedScopus = document.getElementById('scopus-filter').checked;
      const selectedWoS = document.getElementById('wos-filter').checked;
      const selectedRinc = document.getElementById('rinc-filter').checked;
      const selectedVak = document.getElementById('vak-filter').checked;
      const selectedQ1 = document.getElementById('q1-filter').checked;
      const selectedQ2 = document.getElementById('q2-filter').checked;
      const selectedQ3 = document.getElementById('q3-filter').checked;
      const selectedQ4 = document.getElementById('q4-filter').checked;
      const selectedK1 = document.getElementById('k1-filter').checked;
      const selectedK2 = document.getElementById('k2-filter').checked;
      const selectedK3 = document.getElementById('k3-filter').checked;


      for (let i = 0; i < tableRows.length; i++) {
        const row = tableRows[i];
        const name = row.cells[1].textContent.toLowerCase();
        const specialty = row.cells[10].textContent.toLowerCase();
        const scopusValue = row.cells[3].textContent.toLowerCase();
        const scopusValue1 = row.cells[4].textContent.toLowerCase();
        const wosValue = row.cells[5].textContent.toLowerCase();
        const wosValue1 = row.cells[6].textContent.toLowerCase();
        const rincValue = row.cells[7].textContent.toLowerCase();
        const rincValue1 = row.cells[8].textContent.toLowerCase();
        const vakValue = row.cells[9].textContent.toLowerCase();
        const quartileScopusValue = row.cells[4].textContent.toLowerCase();
        const quartileWosValue = row.cells[6].textContent.toLowerCase();
        const combinedQuartileValue = quartileScopusValue + quartileWosValue;
        const combinedScopus = scopusValue + scopusValue1;
        const combinedWos = wosValue + wosValue1;
        const combinedRinc = rincValue + rincValue1;
        const quartileRincValue = row.cells[8].textContent.toLowerCase();
        const combinedQuartileValue1 = quartileRincValue + vakValue;
        const nameMatch = name.includes(nameFilterValue);
        const specialtyMatch = specialty.includes(specialtyFilterValue);

        const dbMatch =
          (!selectedScopus || combinedScopus != "") &&
          (!selectedWoS || combinedWos != '') &&
          (!selectedRinc || combinedRinc != '') &&
          (!selectedVak || vakValue != '');
        const quartileMatch =
(!selectedQ1 || quartileScopusValue == 'q1') &&
  (!selectedQ2 || combinedQuartileValue == 'q2') &&
  (!selectedQ3 || combinedQuartileValue == 'q3') &&
  (!selectedQ4 || combinedQuartileValue == 'q4') &&

  (!selectedK1 || combinedQuartileValue1 == 'k1' || combinedQuartileValue1 == 'к1') &&
  (!selectedK2 || combinedQuartileValue1 == 'k2' || combinedQuartileValue1 == 'к2') &&
  (!selectedK3 || combinedQuartileValue1 == 'k3' || combinedQuartileValue1 == 'к3');
        if (nameMatch && specialtyMatch && quartileMatch && dbMatch) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      }
    }
  });


