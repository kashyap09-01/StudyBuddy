$(document).ready(function () {

    $('.downloadBtn').on('click',function(){
        $('.contentgt').printThis();

      });

    $('.refreshBtn').click(function() {
        // Reload the page
        location.reload();
      });

});