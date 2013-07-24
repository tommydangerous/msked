$(document).ready(function() {
  $(document).on('click', '.station', function() {
    window.location.href = $(this).attr('href');
  });
});