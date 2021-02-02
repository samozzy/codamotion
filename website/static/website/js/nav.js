// Navigation Scripts to Show Header on Scroll-Up

jQuery(document).ready(function($) {
    var lg_brkpoint = 992;

    if ($(window).width() > lg_brkpoint) {
        // Run it at the beginning, and then run it for each scroll event
        function set_classes(currentTop=$(window).scrollTop()) {
            if (currentTop > 0) {
                // if the user has scrolled down
                $('.codamotion-nav').addClass('bg-light').addClass('navbar-light').removeClass('navbar-dark')
                $('#navbar-logo').attr('src', logo_blue);
            } else {
                // if the user is back at the top 
                $('.codamotion-nav').removeClass('bg-light').addClass('navbar-dark').removeClass('navbar-light')
                $('#navbar-logo').attr('src', logo_light);
            }
            return 
        };
        var firstTop = $(window).scrollTop();
        set_classes(firstTop);

        $(window).on('scroll', {
                previousTop: 0
            },
            function() {
                var currentTop = $(window).scrollTop();
                set_classes(currentTop);

                this.previousTop = currentTop;
            }
        );
    }
});