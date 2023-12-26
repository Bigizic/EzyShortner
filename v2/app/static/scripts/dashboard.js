const $ = window.$;
const BASEURL = 'ezyurl.xyz';
const testEnv = 'api/ezy_v1/short?url=';

$(document).ready(() => {


  function opacityStart() {
    $('header').css('opacity', '0.2');
    $('.user_interface').css('opacity', '0.2');
    $('.main-content').css('opacity', '0.2');
    $('.left-sidebar').css('opacity', '0.2');
    $('footer').css('opacity', '0.2');
  };
  
  function opacityEnd() {
    $('header').css('opacity', '1');
    $('.user_interface').css('opacity', '1');
    $('.main-content').css('opacity', '1');
    $('.left-sidebar').css('opacity', '1');
    $('.second_interface').css('opacity', '1');
    $('footer').css('opacity', '1');
  };


  /* start loading view */
  $('.loader').show();
  setTimeout(function() {
    $('.loader-container').fadeOut();
    $('body').css('visibility', 'visible');
  }, 1000);
  /* end loading view */
  
  $('.left-items-li').addClass('hover-effect');
  
  /* Function to add a class for mobile*/
  function addClassForMobile() {
    const leftItemLix = $('.left-items-li');
    if ($(window).width() <= 991) {
      leftItemLix.addClass('mobile-class');
    } else {
      leftItemLix.removeClass('mobile-class');
    }
  }
  /* end class for mobile*/

  /* mobile menu button */
  $('.menu-button').click(function () {
    opacityStart();
    $('.cover-up').css('width', '80%');
  });

  $('.close-button').click(function () {
    opacityEnd();
    $('.cover-up').css('width', '0');
  });
  /* end mobile menu button */

  $('#user_input').keypress(function (e) {
    if (e.which === 13 && $('#user_input').val().length > 3) {
      $('#url_form').submit();
    }
    if (e.which === 13) {
      if ($('#user_input').val().length < 2) {
        $('#user_input').focus();
        $('#user_input').blur();
      }
    }
  });

  $('#user_input').on('input', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
  });

  /* copy button */
  $('.copy_').click(function () {
    const urlField = $('#user_output').select();
    document.execCommand('copy');
    urlField.blur();
  });
  /* end copy button */

  /* qr image animation */
  $('.qr_code').click(function () {
    $('#qr_container').slideDown();
    opacityStart();
  });
  $('#cancelButton').click(function () {
    $('#qr_container').slideUp();
    opacityEnd();
  });
  /* end qr image animation */

  /* output or alias prefered characters */
  $('#user_output').on('input', function() {
    $(this).val($(this).val().replace(/[^a-zA-Z0-9-_+=&]/g, ''));
  });
  /* end prefered characters */

  /* This sets the alias button */
  let isAliasActive = false;
  
  $('.alias').on('click', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
    
    const currentWidth = parseInt($('#user_output').css('width'));
    const lPadd = parseInt($('#user_output').css('padding-left'));
    const rPadd = parseInt($('#user_output').css('padding-right'));
    const newWidth = currentWidth - (lPadd + rPadd);
    if (!isAliasActive) {
      $('#user_output').css('width', newWidth);
      $('#user_output').attr('autofocus', 'autofocus');
      $('#user_output').removeAttr('readonly');
      $('#user_output').attr('placeholder', 'Enter an alias e.g JohnDoe');
      $('.label_user_output').css('color', 'aliceblue');
      $('.label_user_output').css('font-size', 'medium');
      $('.label_user_output').html(BASEURL + '/');
      $('#user_output').on('input', function () {
        const userInput = $(this).val();
        $('.label_user_output').text(`${BASEURL}/` + userInput);
      });
      isAliasActive = true;
    } else {
      const formerWidth = currentWidth + (lPadd + rPadd);
      $('#user_output').val('');
      $('#user_output').css('width', formerWidth);
      $('#user_output').attr('readonly', 'readonly');
      $('#user_output').attr('placeholder', '');
      $('.label_user_output').css('color', '');
      $('.label_user_output').css('font-size', '');
      $('.label_user_output').html('');
      $('#user_output').off('input');

      isAliasActive = false;
    }
  });
  /* end alias button */
  
  /*share animation*/
  $('.b_share').click(function () {
    $('#share_container').slideDown();
    opacityStart();
  });
  $('#cancel-Button').click(function () {
    $('#share_container').slideUp();
    opacityEnd();
  });
  
  /* Share copy little trick */
  $(document).on('click', '#share_copy', function() {
    const parent = $('#user_output').select();
    document.execCommand('copy');
    parent.blur();
    
    $('#warning').text('Copied!');
    setTimeout(() => {
      $('#warning').text('');
    }, 1000);
  });
  /* end share copy littele trick */
  
  
  /* SHARE INTERGRATION */
  const textToShare = $('#user_output').val();
  
  const apps = [
  	['#whatsapp', 'whatsapp'],
  	['#facebook', 'fb'],
  	['#x', 'x'],
  	['#telegram', 'tele'],
  	['#snapchat', 'snap'],
  	['#instagram',  'insta']];
  apps.forEach((element) => {
    $(element[0]).click(function () {
      if (element[0] === '#facebook') {
        $.ajaxSetup({ cache: true });
        $.getScript('https://connect.facebook.net/en_US/sdk.js', function(){
          FB.ui({
            method: 'send',
            link: `${textToShare}`
          });
        });
      } else { shareIntegration(textToShare, element[1]); }
    });
  });
  
  function shareIntegration(textToShare, app) {
    if (app === 'whatsapp') { window.location.href = `whatsapp://send?text=${encodeURIComponent(textToShare)}`; }
    if (app === 'fb') { window.location.href = `fb://share?url=https://ezyurl.xyz&quote=${encodeURIComponent(textToShare)}`; }
    if (app === 'x') {  window.location.href = `xapp://share?message=${encodeURIComponent(textToShare)}`; }
    if (app === 'tele') { window.location.href = `tg://msg?text=${encodeURIComponent(textToShare)}`; }
    if (app === 'snap') { const doSomething = 'Do something'; }
    if (app === 'insta') { window.location.href = `instagram://share?text=${encodeURIComponent(textToShare)}`; }
  }
  /* End share animation*/
  
  

  $('.main-content h1').click(function () {
    window.location.replace(window.location.href);
  });
  addClassForMobile();
  $(window).resize(addClassForMobile);
});
