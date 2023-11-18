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
  });
  $('#cancelButton').click(function () {
    $('#qr_container').slideUp();
  });
  /* end qr image animation */

  $('header h1').click(function () {
    window.location.replace(window.location.href);
  });

  /* history animation */
  $('.history').click(function () {
    $('.history_list').css('width', '24%');
  });
  $('.h-close-button').click(function () {
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
  $('.alias').one('click', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
    const currentWidth = parseInt($('#user_output').css('width'));
    const lPadd = parseInt($('#user_output').css('padding-left'));
    const rPadd = parseInt($('#user_output').css('padding-right'));
    const newWidth = currentWidth - (lPadd + rPadd);
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
  });
  /* end alias button */

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
              const article = `
                <li>
                <h3>${item.original_url} <button class="history_copy">Copy</button></h3>
                <ul>
                  <li class="short-url-history">
                    Short URL: https://ezyurl.xyz/${item.short_url} <button class="history_copy">Copy</button><br>
                    Created At: ${item.created_at}<br>
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
});
