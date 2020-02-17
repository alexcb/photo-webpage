var orig_widths = {};
function resize_images() {
  console.log('hello');

  var max_width = $('#container').width();

  var images = $('div.blog img');
  $.each(images, function(i, img) {
    var iw = img.width;
    if( iw > 0 ) {
      if( !(img.url in orig_widths) ) {
        orig_widths[img.url] = img.width;
      }
      iw = orig_widths[img.url];
      if( img.width >= max_width || iw > max_width ) {
        iw = max_width;
      }
      if( iw > 0 ) {
        $(img).css({'width' : iw + 'px'});
      }
    }
  });
}

$(window).resize(function () { resize_images(); });
$(function() {
  resize_images();
});

$("img").one("load", resize_images );
