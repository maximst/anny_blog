(function($) {
  $(document).ready(function(){
    $('#id_tags').autocomplete({
      serviceUrl: '/tag_autocomplite/',
      minChars: 2,
      delimiter: /(,)\s*/,
      maxHeight: 400,
      width: 300,
      zIndex: 9999,
      deferRequestBy: 100,
      onSelect: function(data, value){
        $(this).val($(this).val() + ', ');
      }
    });
  });
})(django.jQuery.noConflict());