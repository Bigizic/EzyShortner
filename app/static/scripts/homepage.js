const $ = window.$;

$(document).ready(() => {

    $('.enter').click(function () {
        if ( $('.share').css('visibility', 'hidden') === true) {
            $('share'.css('visibility', 'visible'));
        };
    });
});
