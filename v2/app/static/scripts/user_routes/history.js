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
    $('#search_input').attr('placeholder', 'Search by long or short link');
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
    return moment.utc(utcDateTime).tz(userTimezone).format('dddd Do MMMM YYYY HH:mm:ss');
};
/* END */

  $('.table-row .col-2').each(function() {
    let utcTime = $(this).text();
    let localTime = convertUTCToLocal(utcTime);
    $(this).text(localTime);
  });
  
  
  /*DELETE BUTTON FUNCTIONS */
  
  $('.delete-btn').on('click', function(e) {
    e.preventDefault();
    let ezyUrlId = $(this).data('ezy-url-id');
    if (confirm('Are you sure you want to delete this record?')) {
      $.ajax({
        url: `/history/delete/${ezyUrlId}`,
        method: 'POST',
        success: function(response) {
          window.location.replace(window.location.href);
        },
        error: function(xhr, status, error) {
          console.error(error);
        }
      });
    }
  });
  /*END DELETE BUTTON */
  
  /* output or alias prefered characters */
  $('#search_input').on('input', function() {
    $(this).val($(this).val().replace(/[' ']/g, ''));
  });
  /* end prefered characters */

  /* status code NOT FOUND */
  const statusElement = $('#status_code');
    if (statusElement.length) {
      setTimeout(function () {
        statusElement.fadeOut();
      }, 3000);
    }
  /* end */
  
  $('.main-content h1').click(function () {
    window.location.replace(window.location.href);
  });
});
