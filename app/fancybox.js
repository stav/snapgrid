// Fancybox binding
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    Fancybox.bind('[data-fancybox]', {
      on: {
        // When the Fancybox is opened, set the snapgridFilename data attribute on the container.
        // This is used to open the Markdown dialog with the correct filename.
        done: (fancybox, slide) => {
          fancybox.container.setAttribute(
            'data-snapgridFilename',
            slide.snapgridFilename
          );
        },
      },
    });
  });
})(); // IIFE
