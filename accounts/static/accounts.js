/*global $ */

var initialize = function (navigator, user, token, urls) {
    $('#id_login').on('click', function() {
        navigator.id.request();
    });

    navigator.id.watch({
        loggedInUser: user,
        onlogin: function (assertion) {
            $.ajax({
                method: 'POST',
                url: urls.login,
                data: {
                    assertion: assertion,
                    csrfmiddlewaretoken: token,
                },
            })
            .done(function () { window.location.reload(); })
            .fail(function () { navigator.id.logout(); });
        },
        onlogout: function () {},
    });
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
