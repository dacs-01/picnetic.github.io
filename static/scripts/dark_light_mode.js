$(document).ready(function() {
    if (sessionStorage.getItem("isDarkMode") == 1){
        $( "header" ).addClass( "header_dark" );
        $( "body" ).addClass( "body_dark" );
        $( "footer" ).addClass( "footer_dark" );
    }
    $( ".change" ).on("click", function() {
        if( sessionStorage.getItem("isDarkMode") == 1) {
            $( "header" ).removeClass( "header_dark" )
            $( "body" ).removeClass( "body_dark" );
            $( "footer" ).removeClass( "footer_dark" );
            $( ".change" ).text( "OFF" );
            sessionStorage.setItem("isDarkMode", 0);
        } else {
            $( "header" ).addClass( "header_dark" );
            $( "body" ).addClass( "body_dark" );
            $( "footer" ).addClass( "footer_dark" );
            $( ".change" ).text( "ON" );
            sessionStorage.setItem("isDarkMode", 1);
        }
    });
});