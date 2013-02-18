$(document).ready(function() {
    $(document).on('mouseover', '.account', function() {
        $(this).addClass('menuShow');
        $('#menu').show();
        return false;
    });
    $(document).on('mouseover', '#menu', function() {
        return false;
    });
    $(document).on('mouseover', $(document), function() {
        $('.account').removeClass('menuShow');
        $('#menu').hide();
    });
});