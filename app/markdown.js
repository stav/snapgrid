(function () {
  let dialog;
  document.addEventListener('DOMContentLoaded', function () {
    dialog = document.querySelector('#markdown-dialog');
  });

  // Add keyboard event listener for Markdown dialog
  document.addEventListener('keydown', function (event) {
    // Close the Markdown dialog
    if (event.key === 'c') {
      if (dialog) {
        dialog.style.display = 'none';
      }
    }
    // Open the Markdown dialog if the Fancybox dialog is open
    const fancybox = document.querySelector(
      '.fancybox__container[role="dialog"]'
    );
    if (fancybox) {
      if (event.key === 'd') {
        if (dialog) {
          dialog.style.display = 'block';
          // Set the filename in the dialog
          const filename = fancybox.getAttribute('data-snapgridFilename');
          const markdownFilename = dialog.querySelector('.markdown-filename');
          markdownFilename.textContent = filename;
          const markdownContent = dialog.querySelector('.markdown-content');
          
          // Fetch markdown content from the server
          fetch(`/markdown/${filename}/`)
            .then(response => response.text())
            .then(content => {
              markdownContent.innerHTML = content;
            })
            .catch(error => {
              markdownContent.innerHTML = '<p>Error loading markdown content.</p>';
              console.error('Error fetching markdown:', error);
            });
        }
      }
    }
  });
})(); // IIFE
