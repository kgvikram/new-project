console.log('js loaded')
$(function() {

    console.log( "ready!" );


     $('#datepicker').datepicker({          
            format: "yyyy",
            viewMode: "years",
            minViewMode: "years",
            orientation: "auto"

           });
});


