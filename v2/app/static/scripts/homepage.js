const $ = window.$;
const BASEURL = 'ezyurl.xyz';
const testEnv = 'api/ezy_v1/short?url=';

$(document).ready(() => {


  function opacityStart() {
    $('header').css('opacity', '0.2');
    $('.user_interface').css('opacity', '0.2');
    $('.second_interface').css('opacity', '0.2');
    $('footer').css('opacity', '0.2');
  };
  
  function opacityEnd() {
    $('header').css('opacity', '1');
    $('.user_interface').css('opacity', '1');
    $('.second_interface').css('opacity', '1');
    $('footer').css('opacity', '1');
  };


  /* start loading view */
  $('.loader').show();
  setTimeout(function() {
    $('.loader-container').fadeOut();
    $('body').css('visibility', 'visible');
  }, 3000);
  /* end loading view */


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
    opacityStart();
    $('#qr_container').slideDown();
  });
  $('#cancelButton').click(function () {
    opacityEnd();
    $('#qr_container').slideUp();
  });
  /* end qr image animation */

  $('header h1').click(function () {
    window.location.replace(window.location.href);
  });
  $('.mobile_h1').click(function () {
    window.location.replace(window.location.href);
  });

  /* history animation for desktops && larger screens*/
  $('.history').click(function () {
    $('.user_interface').css('opacity', '0.2');
    $('.second_interface').css('opacity', '0.2');
    $('footer').css('opacity', '0.2');
    $('.history_list').css('width', '24%');
  });
  $('.h-close-button').click(function () {
    $('.user_interface').css('opacity', '1');
    $('.second_interface').css('opacity', '1');
    $('footer').css('opacity', '1');
    $('.history_list').css('width', '0%');
  });
  /* end history animation */

  /* mobile menu button */
  $('.menu-button').click(function () {
    $('.cover-up').css('width', '80%');
  });

  $('.close-button').click(function () {
    $('.cover-up').css('width', '0');
  });
  /* end mobile menu button */

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
      $('#user_output').attr('placeholder', 'Enter an alias e.g ezyurl.xyz/awesome-tips');
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
  
  
/* FUNCTION TO GET CURRENT TIMEZONE OF A USER AND USE IT TO UPDATE CREATED FIELD IN HISTORY SECTION*/
  function convertUTCToLocal(utcDateTime) {
    let userTimezone = moment.tz.guess();
    return moment.utc(utcDateTime).tz(userTimezone).format('dddd Do MMMM YYYY HH:mm:ss');
};
/* END */


  /* histroy section */
  let userHistory = JSON.parse(localStorage.getItem('userHistory')) || [];

  function updateHistory(userInput) {
    userHistory.push(userInput);
    
    localStorage.setItem('userHistory', JSON.stringify(userHistory));
  };

  $('.history').click(function() {
    let storedUserHistory = JSON.parse(localStorage.getItem('userHistory'));
    const historyList = $('.long-url-history');
    //$('.short-url-history').empty();
    historyList.empty();
    
    if (storedUserHistory) {
      storedUserHistory.forEach(function(userInput) {
        //$('.short-url-history').append('<li>' + userInput + '</li>');
        $.ajax({
          url: `${testEnv}` + userInput,
          type: 'GET',
          success: function(result) {
            const historyList = $('.long-url-history');
            for (let item of result.data) {
              const user_time = convertUTCToLocal(item.created_at);
              const article = `
                <li>
                <h3>${item.original_url} <button class="history_copy">Copy</button></h3>
                <ul>
                  <li class="short-url-history">
                    <strong>Short URL:</strong> https://ezyurl.xyz/${item.short_url} <button class="history_copy">Copy</button><br>
                    <strong>Created At:</strong> ${user_time}<br>
                  </li>
                </ul>
                </li>`;
              historyList.append(article);           
            }
          },
          error: function(err) { console.log(err); }
	});
      });
    } else {
        const article = `
	  <li class="history_nothing_list">
          <h3 class="history_nothing">Nothing to see here
          </h3>
          </li>`;
        $('.long-url-history').append(article);
    };
  });

  let userInput = $('#user_output').val();
  if (userInput) {
    updateHistory(userInput);
  }
  /* end history section */




  /*history onclick operations */
  $(document).on('click', '.history_copy', function() {
    const parent = $(this).parent();
    if (parent.is('h3')) {
      const textToCopy = parent.text().trim().split(' ')[0];
      copyTextToClipboard(textToCopy);
    } else if ( parent.is('.short-url-history') ) {
        const textToCopy = parent.text().trim().split(' ')[2];
        copyTextToClipboard(textToCopy);
    }
    $(this).text('Copied!');
    setTimeout(() => {
      $(this).text('Copy');
    }, 1000);
  });
  function copyTextToClipboard(text) {
    const tempTextarea = document.createElement('textarea');
    tempTextarea.value = text;

    document.body.appendChild(tempTextarea);
    tempTextarea.select();
    document.execCommand('copy');
    document.body.removeChild(tempTextarea);
  };
  /* end history onclick operations */


  /* start mobile history view */
  $('.menu-information .history').click(function () {
    $('.menu-information .history_list').css('width', '100%');
  });
  $('.menu-information .h-close-button').click(function () {
    $('.menu-information .history_list').css('width', '0%');
  });
  /* end mobile history view */
  
  /* product hover + button */
  $('.first_product, .second_product, .third_product').hover(
    function() {
      $(this).find('a button').removeClass('remove-effect').addClass('hover-effect');
    },
    function() {
      $(this).find('a button').removeClass('hover-effect').addClass('remove-effect');
    }
  );
  /* end product hover + button*/
  
  
  /*share animation*/
  $('.b_share').click(function () {
    opacityStart();
    $('#share_container').slideDown();
  });
  $('#cancel-Button').click(function () {
    opacityEnd();
    $('#share_container').slideUp();
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
});
