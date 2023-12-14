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
  
  if (window.currentFile === "fileA") {
    $('.left-items-lix').addClass('hover-effect');
  } else {
    $('.left-items-liii').addClass('hover-effect');
  }

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
    if (window.currentFile === "fileA") {
      const leftItemLix = $('.left-items-lix');
      if ($(window).width() <= 991) {
        leftItemLix.addClass('mobile-class');
      } else {
        leftItemLix.removeClass('mobile-class');
      }
    } else {
      if ($(window).width() <= 991) {
        $('.left-items-liii').addClass('mobile-class');
      } else {
        $('.left-items-liii').removeClass('mobile-class');
      }
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
  
  /* GRAPH */
  const records = [];

  $('.table-row').each(function() {
    const shortUrl = $(this).find('.col-4').text().trim();
    const clicks = parseInt($(this).find('.col-5').text().trim(), 10);

    const record = { url: shortUrl, clicks: clicks };
    records.push(record);
    records.sort((a, b) => b.clicks - a.clicks);
  });
  const clicksData = records.slice(0, 10).map(record => record.clicks);
  const shortUrlData = records.slice(0, 10).map(record => record.url);

  const ctx = $('#userChart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: shortUrlData,
      datasets: [{
        label: 'No of Clicks',
        data: clicksData,
        borderWidth: 1,
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            color: 'white'
          }
        },
        x: {
          ticks: {
            color: 'white'
          }
        }
      }
    }
  });
  
  /* END GRAPH */
  
  
  /* EDIT YOUR LINKS FILE */
  
  /* long link edit form show() */
  $('.bi-pen-fill').on('click', function (e) {
    let shortLink = $(this).parent().find('.col-4').data('short-link');
    $('#short_link').val('https://ezyurl.xyz/' + shortLink);
    $('.editlink_form').slideDown();
  });
  $('#pass_cancel').click(function () {
    $('.editlink_form').slideUp();
  });
  /* End long link edit form */
  
  /* status code color */
  if ($('#status_code').html() === 'Successfully updated') {
    $('#status_code').css('color', '#007400');
  } else {
    $('#status_code').css('color', 'red');
  }
  /* end status code color */
  
  
  /* END EDIT YOUR LINKS FILE*/
});
