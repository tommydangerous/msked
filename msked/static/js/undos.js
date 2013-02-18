$(document).ready(function() {
    $(document).on('click', '.undo a', function() {
        var confirm = $('.confirmDelete');
        var url = $(this).attr('href');
        confirm.dialog({
            height: 100,
            resizeable: false,
            buttons: {
                'Delete': function() {
                    window.location.href = url;
                },
                Cancel: function() {
                    confirm.dialog('close');
                }
            }
        })
        return false;
    })
})