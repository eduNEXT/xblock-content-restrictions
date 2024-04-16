/* Javascript for XblockContentRestrictions. */
function XblockContentRestrictions(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, 'has_access_with_password');

    let gettext;
    if ("ContentRestrictionsI18N" in window || "gettext" in window) {
      gettext = window.ContentRestrictionsI18N?.gettext || window.gettext;
    }

    if (typeof gettext == "undefined") {
      // No translations -- used by test environment
      gettext = (string) => string;
    }

    $(element).find('.submit-button').bind('click', function() {
        var data = {
            "password": $(element).find('input[name=password]').val(),
        }
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.success) {
                window.location.reload(false);
            }
            else {
                $(element).find('.incorrect_password_explanation_text').text(gettext(response.error_message));
            }
        }
        );
    })
}
