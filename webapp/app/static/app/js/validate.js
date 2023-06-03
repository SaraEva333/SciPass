const titleField = document.getElementById('title');
const ISSNField = document.getElementById('issn');
const ifValueField = document.getElementById('if_value');
const dbIFField = document.getElementById('db_if');
const yearIfField = document.getElementById('year_if');
const quartField = document.getElementById('current_quartile');
const dbQuartField = document.getElementById('db_quart');
const yearQuartField = document.getElementById('year_quart');
const codeField = document.getElementById('code');
const datField = document.getElementById('dat');
const form = document.querySelector('form');
const submitButton1 = document.getElementById('submit1');

submitButton1.addEventListener('click', function(event) {
  event.preventDefault();
  validateAndSubmitForm();
});
function validateAndSubmitForm() {
  if (!validateData()) {
    return;
  }

  form.submit();
}

function validateData() {
  const errorField = form.querySelector('.error-message');

  if (!validateQuartileSelection()) {
    errorField.textContent = "! Выберите правильные квартили в зависимости от выбранной базы данных!";
    return false;
  }

  if (!validateISSN()) {
    errorField.textContent = '! Введите ISSN форматом XXXXXXXX ';
    return false;
  }

  if (!validateIfValue()) {
    errorField.textContent = '! Импакт-фактор не может быть таким большим или он введен не по формату X.XXX';
    return false;
  }

  if (!validateYearIf()) {
    errorField.textContent = '! Год обновления импакт-фактора не соответствует требованиям, введите год форматом ХХХХ';
    return false;
  }

  if (!validateYearQuart()) {
    errorField.textContent = '! Год обновления квартиля не соответствует требованиям, введите год форматом ХХХХ';
    return false;
  }

  if (!validateCode()) {
    errorField.textContent = '! Введите год специальности форматом 1.2.3.';
    return false;
  }

  if (!validateDat()) {
    errorField.textContent = '! Дата обновления специальности не соответствует требованиям';
    return false;
  }

  errorField.textContent = '';
  return true;
}

function validateTitle() {
  const value = titleField.value.trim();

  return value.length > 0 && value.length <= 200;
}

function validateISSN() {
  const value = ISSNField.value.trim();

  if (value === "") {
    return true; // Skip validation if the value is empty
  }

  if (!/^[0-9]{7}[0-9Х]$/.test(value)) {
    return false;
  }

  return true;
}

function validateIfValue() {
  const value = ifValueField.value.trim();
    if (value === "") {
    return true; // Skip validation if the value is empty
  }
  const numericRegex = /^(\d+([.,]\d{1,3})?)$/;

  if (!numericRegex.test(value)) {
    return false;
  }

  const numericValue = parseFloat(value.replace(',', '.'));
  return numericValue <= 99;
}

function validateYearIf() {
  const value = yearIfField.value.trim();
    if (value === "0") {
    return true; // Skip validation if the value is empty
  }
  const currentYear = new Date().getFullYear();

  if (value < 1900 || value > 2024) {
    return false;
  }

  return /^[0-9]{4}$/.test(value);
}

function validateYearQuart() {
  const value = yearQuartField.value.trim();
    if (value === "0") {
    return true; // Skip validation if the value is empty
  }
  const currentYear = new Date().getFullYear();

  if (value < 1900 || value > 2024) {
    return false;
  }

  return /^[0-9]{4}$/.test(value);
}

function validateCode() {
  const value = codeField.value.trim();
    if (value === "") {
    return true; // Skip validation if the value is empty
  }
  return /^\d{1,3}\.\d{1,3}\.\d{1,3}\.$/.test(value);
}

function validateDat() {
  const value = datField.value.trim();
    if (value === "") {
    return true; // Skip validation if the value is empty
  }
  const dateRegex = /^(\d{1,2})\.(\d{1,2})\.(\d{2})$/;

  if (!dateRegex.test(value)) {
    return true;
  }

  const [, day, month, year] = value.match(dateRegex);
  const currentYear = new Date().getFullYear();
  const parsedYear = parseInt(year, 10) + (parseInt(year, 10) > 30 ? 1900 : 2000);
  const currentDate = new Date();
  const selectedDate = new Date(parsedYear, parseInt(month, 10) - 1, parseInt(day, 10));

  datField.max = currentDate.toISOString().split('T')[0];

  const errorSpan = document.getElementById('error-message');

  if (selectedDate.getTime() > currentDate.getTime()) {
    errorSpan.textContent = 'Выберите дату, которая не превышает текущую дату.';
    return false;
  }

  errorSpan.textContent = '';

  return parsedYear >= 1900 && parsedYear <= currentYear && parseInt(month, 10) <= 12 && parseInt(day, 10) <= new Date(parsedYear, parseInt(month, 10), 0).getDate();
}

function validateQuartileSelection() {
  const dbQuart = dbQuartField.value;
  const currentQuartile = quartField.value;

  if ((dbQuart === "Scopus" || dbQuart === "WoS") && currentQuartile !== "Q1" && currentQuartile !== "Q2" && currentQuartile !== "Q3" && currentQuartile !== "Q4") {
    return false;
  } else if ((dbQuart === "РИНЦ" || dbQuart === "ВАК") && currentQuartile !== "K1" && currentQuartile !== "K2" && currentQuartile !== "K3") {
    return false;
  }

  return true;
}
