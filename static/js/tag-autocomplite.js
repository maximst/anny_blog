(function($) {
  $(document).ready(function(){
    var $searchBox = $('#id_tags');
    $searchBox.autocomplete({
      serviceUrl: '/tag_autocomplite/',
      minChars: 2,
      delimiter: /(,)\s*/,
      maxHeight: 400,
      width: 300,
      zIndex: 9999,
      deferRequestBy: 100
    });
  });
})(django.jQuery.noConflict());