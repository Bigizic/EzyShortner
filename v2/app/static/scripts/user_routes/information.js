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
  $('.left-items-lx').addClass('hover-effect');
  
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
    const leftItemLix = $('.left-items-lx');
    if ($(window).width() <= 991) {
      leftItemLix.addClass('mobile-class');
    } else {
      leftItemLix.removeClass('mobile-class');
    }
  }
  /* end class for mobile*/


  addClassForMobile();
  $(window).resize(addClassForMobile);
  
  
});
