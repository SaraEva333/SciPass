//         <button class="action-button0" id="add-row-button"><span class="plus-icon">+</span></button>        Получаем ссылку на таблицу и кнопку "Добавить строку"

var table = document.getElementById('journal-table');
var addRowButton = document.getElementById('add-row-button');

// Обработчик события для кнопки "Добавить строку"
addRowButton.addEventListener('click', function() {
  // Создаем новую строку и ячейки
  var newRow = table.insertRow();
  var cell1 = newRow.insertCell();
  var cell2 = newRow.insertCell();
  var cell3 = newRow.insertCell();
  var cell4 = newRow.insertCell();
  var cell5 = newRow.insertCell();
  var cell6 = newRow.insertCell();
  var cell7 = newRow.insertCell();
  var cell8 = newRow.insertCell();
  var cell9 = newRow.insertCell();
  var cell10 = newRow.insertCell();
  var cell11 = newRow.insertCell();
  // Добавьте ячейки для остальных столбцов по необходимости

  // Устанавливаем атрибут contenteditable для ячеек, чтобы они были редактируемыми
  cell1.setAttribute('contenteditable', 'true');
  cell2.setAttribute('contenteditable', 'true');
  cell3.setAttribute('contenteditable', 'true');
  cell4.setAttribute('contenteditable', 'true');
  cell5.setAttribute('contenteditable', 'true');
  cell6.setAttribute('contenteditable', 'true');
  cell7.setAttribute('contenteditable', 'true');
  cell8.setAttribute('contenteditable', 'true');
  cell9.setAttribute('contenteditable', 'true');
  cell10.setAttribute('contenteditable', 'true');
  cell11.setAttribute('contenteditable', 'true');


  // Установите атрибуты contenteditable для остальных ячеек по необходимости

  // Добавляем новые элементы в HTML-разметку таблицы
  newRow.appendChild(cell1);
  newRow.appendChild(cell2);
  newRow.appendChild(cell3);
  newRow.appendChild(cell4);
  newRow.appendChild(cell5);
  newRow.appendChild(cell6);
  newRow.appendChild(cell7);
  newRow.appendChild(cell8);
  newRow.appendChild(cell9);
  newRow.appendChild(cell10);
  newRow.appendChild(cell11);
  // Добавьте остальные ячейки в строку по необходимости
});
