function openPDF() {
  const fileInput = document.getElementById('pdf-input');
  fileInput.click();
}

function handlePDFFile(event) {
  const file = event.target.files[0];
  const fileName = file.name; // Get the file name

  // Create a FormData object and append the file to it
  const formData = new FormData();
  formData.append('pdf_file1', file);

  // Retrieve the CSRF token from the cookies
  const csrftoken = getCookie('csrftoken');

  // Include the CSRF token in the request headers
  fetch('/addPDF', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: formData
  })
    .then(response => {
      // Handle the response from the server
      if (response.ok) {
        // If the response is successful, reload the page to display the updated data
        window.location.reload();
      } else {
        // If the response is not successful, handle the error
        throw new Error('Error uploading PDF file.');
      }
    })
    .catch(error => {
      // Handle any errors
      console.error(error);
    });
}

// Helper function to retrieve the CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Attach the event handler to the file input element
document.getElementById('pdf-input').addEventListener('change', handlePDFFile);

function openPDF() {
  const fileInput = document.getElementById('pdf-input');
  fileInput.click();
}

function handlePDFFile1(event) {
  const file = event.target.files[0];
  const fileName = file.name; // Get the file name

  // Create a FormData object and append the file to it
  const formData = new FormData();
  formData.append('pdf_file1', file);

  // Retrieve the CSRF token from the cookies
  const csrftoken = getCookie('csrftoken');

  // Include the CSRF token in the request headers
  fetch('/addPDF', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    body: formData
  })
    .then(response => {
      // Handle the response from the server
      if (response.ok) {
        // If the response is successful, reload the page to display the updated data
        window.location.reload();
      } else {
        // If the response is not successful, handle the error
        throw new Error('Error uploading PDF file.');
      }
    })
    .catch(error => {
      // Handle any errors
      console.error(error);
    });
}

// Helper function to retrieve the CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Attach the event handler to the file input element
document.getElementById('pdf-input1').addEventListener('change', handlePDFFile1);

