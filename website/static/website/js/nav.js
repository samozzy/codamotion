// Make the header background change when the user scrolls down
// (and reset when they reach the top again!)

jQuery(document).ready(function($) {
    var lg_brkpoint = 992;

    if ($(window).width() > lg_brkpoint) {
        // The heavy lifting 
        // The logo sources are defined in base.html so we can use Django static tags
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

        // Run at page load...
        set_classes(firstTop);

        // ... and then for each scroll event
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