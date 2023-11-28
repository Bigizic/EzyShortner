const $ = window.$;
const BASEURL = 'ezyurl.xyz';
const testEnv = 'api/ezy_v1/short?url=';

$(document).ready(() => {

  /* start loading view */
  $('.loader').show();
  setTimeout(function() {
    $('.loader-container').fadeOut();
    $('body').css('visibility', 'visible');
  }, 1000);
  /* end loading view */
  $('.left-items-lix').addClass('hover-effect');
  
  /* SEARCH */
  
  var app = $("#app"),
    short = $("#short_"),
    long = $("#long_"),
    input = $("#inp-cover input"),
    button = $("button");

  function toggleApp() {
    app.toggleClass("opened");

    if (button.hasClass("shadow")) button.toggleClass("shadow");
    else
      setTimeout(function () {
        button.toggleClass("shadow");
      }, 300);

    if (app.hasClass("opened")) {
      setTimeout(function () {
        input.toggleClass("move-up");
      }, 200);
      setTimeout(function () {
        input.focus();
      }, 500);
    } else
      setTimeout(function () {
        input.toggleClass("move-up").val("");
      }, 200);

    if (!long.hasClass("sl")) {
      setTimeout(function () {
        long.addClass("sl");
      }, 800);
    } else
      setTimeout(function () {
        long.removeClass("sl");
      }, 300);
  }

  long.click(function() {
    toggleApp();
    $('#search_input').attr('placeholder', 'Enter a long link e.g Example.com/this-is-an-example');
  });

  short.click(function() {
    toggleApp();
    $('#search_input').attr('placeholder', 'Enter a short link e.g https://ezyurl.xyz/a-link');
  });

  /* END SEARCH */
  
  /* mobile menu button */
  $('.menu-button').click(function () {
    $('.cover-up').css('width', '80%');
  });

  $('.close-button').click(function () {
    $('.cover-up').css('width', '0');
  });
  /* end mobile menu button */
  
  /* BEGIN HISTORY ITEMS */
  /* END HISTORY ITEMS */
  
  
  
  /* Function to add a class for mobile*/
  function addClassForMobile() {
    const leftItemLix = $('.left-items-lix');
    if ($(window).width() <= 991) {
      leftItemLix.addClass('mobile-class');
    } else {
      leftItemLix.removeClass('mobile-class');
    }
  }
  /* end class for mobile*/


  addClassForMobile();
  $(window).resize(addClassForMobile);
  
  
  /* FUNCTION TO GET CURRENT TIMEZONE OF A USER AND USE IT TO UPDATE CREATED FIELD IN HISTORY SECTION*/
  function convertUTCToLocal(utcDateTime) {
    let userTimezone = moment.tz.guess();
    return moment.utc(utcDateTime).tz(userTimezone).format('dddd MMMM YYYY HH:mm:ss');
};
/* END */

  $('.table-row .col-2').each(function() {
    let utcTime = $(this).text();
    let localTime = convertUTCToLocal(utcTime);
    $(this).text(localTime);
  });
});
