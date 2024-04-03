/* Javascript for XblockContentRestrictions. */
function XblockContentRestrictions(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'has_access_with_password');

    $(element).find('.submit-button').bind('click', function() {
        var data = {
            "password": $(element).find('input[name=password]').val(),
        }
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.success) {
                window.location.reload(false);
            }
            else {
                $(element).find('.error-message').text(response.error_message);
            }
        }
        );
    })
}
