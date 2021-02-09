// Make the header background change when the user scrolls down
// (and reset when they reach the top again!)

jQuery(document).ready(function($) {
    function nav_expand() {
        $('.codamotion-nav').addClass('bg-light shadow-sm nav-border-bottom').addClass('navbar-light').removeClass('navbar-dark')
        $('#navbar-logo').attr('src', logo_blue);
        return
    }
    function nav_collapse() {
        $('.codamotion-nav').removeClass('bg-light shadow-sm nav-border-bottom').addClass('navbar-dark').removeClass('navbar-light')
        $('#navbar-logo').attr('src', logo_light);
        return
    }

    // The heavy lifting 
    // The logo sources are defined in base.html so we can use Django static tags
    function set_classes(currentTop=$(window).scrollTop()) {
        if (currentTop > 0) {
            // if the user has scrolled down
            nav_expand();
        } else {
            // if the user is back at the top 
            nav_collapse();
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
    // Special case: make the navbar have a background when expanded on mobile
    $('#coda-nav-expand-toggler').click(function() {
        // If the nav is collapsed and being expanded we should change the class so the text is visible!
        if ($(window).scrollTop() == 0) {
            if ($(this).hasClass('collapsed')) {
                nav_collapse() 
            }else {
                nav_expand();
            }
        }
    });
});