$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/bad_Experience',
            data: {'destination': $('#destination').val()},
            type: 'POST',
            }
        });
    });
});
