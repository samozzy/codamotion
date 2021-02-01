jQuery(document).ready(function() {

    // Click tracking
    jQuery("a[href^='http']").click(function () {
        var target = jQuery(this).attr("href");
        if (target.indexOf("www.codamotion.com") < 0) {
            gtag('event', 'External Link', {
                'event_category': 'click',
                'event_label': target,
                'value': 1
            });
        }
    });

    jQuery("a[href^='tel:']").click(function () {
        gtag('event', 'Phone Number', {
            'event_category': 'click',
            'event_label': jQuery(this).attr('href').replace('tel:', ''),
            'value': 1
        });
    });

    jQuery("a[href^='mailto:']").click(function () {
        gtag('event', 'E-mail address', {
            'event_category': 'click',
            'event_label': jQuery(this).attr('href').replace('mailto:', ''),
            'value': 1
        });
    });

    jQuery("a[href$='.pdf']").click(function () {
        gtag('event', 'PDF download', {
            'event_category': 'click',
            'event_label': jQuery(this).attr('href'),
            'value': 1
        });
    });

});