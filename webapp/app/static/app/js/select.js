function getSelectedRows() {
  const allRows = document.querySelectorAll('.journal-table tbody tr');
  const selectedRows = [];
  allRows.forEach((row, index) => {
    const checkbox = row.querySelector('.select-row');
    if (checkbox.checked) {
      selectedRows.push(index);
    }
  });
  return selectedRows;
}



const selectAllCheckbox = document.getElementById('select-all');
selectAllCheckbox.addEventListener('change', function() {
  const visibleRows = document.querySelectorAll('.journal-table tbody tr:not([style*="display: none"])');
  const checkboxes = document.querySelectorAll('.select-row');
  visibleRows.forEach((row, index) => {
    const checkbox = row.querySelector('.select-row');
    checkbox.checked = selectAllCheckbox.checked;
  });
});

document.getElementById('export-data-btn').addEventListener('click', function() {
  const selectedRows = getSelectedRows();
  if (selectedRows.length > 0) {
    // Перенаправление на страницу экспорта данных с передачей индексов выбранных строк
    const rowIndexes = selectedRows.join(',');
    window.location.href = '/exportData/' + selectedRows;
  } else {
    console.error('Пожалуйста, выберите хотя бы одну строку.');
  }
});
document.getElementById('edit-data-btn').addEventListener('click', function() {
  const selectedRows = getSelectedRows();
  if (selectedRows.length === 1) {
    const rowIndex = selectedRows[0]; // Предполагая, что массив selectedRows содержит индексы выбранных строк

    // Перенаправление на страницу редактирования данных с передачей индекса выбранной строки
    window.location.href = '/edit/' + rowIndex;
  } else {
    console.error('Пожалуйста, выберите только одну строку.');
  }
});

document.getElementById('view-history-btn').addEventListener('click', function() {
  const selectedRows = getSelectedRows();
  if (selectedRows.length === 1) {
    const rowIndex = selectedRows[0]; // Предполагая, что массив selectedRows содержит индексы выбранных строк

    // Перенаправление на страницу редактирования данных с передачей индекса выбранной строки
    window.location.href = '/allData/' + rowIndex;
  } else {
    console.error('Пожалуйста, выберите только одну строку.');
  }
});

document.getElementById('delete-data-btn').addEventListener('click', function() {
  const selectedRows = getSelectedRows();
  if (selectedRows.length === 1) {
    const rowIndex = selectedRows[0]; // Предполагая, что массив selectedRows содержит индексы выбранных строк

    // Перенаправление на страницу редактирования данных с передачей индекса выбранной строки
    window.location.href = '/deleteData/' + rowIndex;
  } else {
    console.error('Пожалуйста, выберите только одну строку.');
  }
});