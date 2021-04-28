function requestWithoutReload(url, data){
     event.preventDefault();
      $.ajax({
         type: "POST",
         url: url,
         data: data,
         success: function() {

          }
     });
}