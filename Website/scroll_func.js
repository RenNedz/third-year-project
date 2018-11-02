//moves header horizontally as user scrolls across

$(window).scroll(function(){
  $('.header').css('right', -$(window).scrollLeft());
});

//keeps search form to left as user scrolls across

$(window).scroll(function(){
  $('#ukform').css('left',-$(window).scrollLeft());
});

$(window).scroll(function(){
  $('#intform').css('left',-$(window).scrollLeft());
});