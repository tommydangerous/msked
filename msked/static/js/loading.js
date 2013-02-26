$(document).ready(function() {
    $(document).on('click', '.scheduleNav a', function() {
        var spinner = new Spinner().spin();
        $('.loading div').append(spinner.el);
        $('.loading').show();
    });
});