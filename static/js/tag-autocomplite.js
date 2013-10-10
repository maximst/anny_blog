(function($) {
  $('#id_tags').autocomplete({
      serviceUrl: '/tag_autocomplite/',
      minChars: 2,
      delimiter: /,\s*/,
      maxHeight: 400,
      width: 300,
      zIndex: 9999,
      deferRequestBy: 100
  //     params: { country: 'Yes'},
  //     onSelect: function(data, value){ },
  //     lookup: ['January', 'February', 'March']
  });
})(django.jQuery.noConflict());