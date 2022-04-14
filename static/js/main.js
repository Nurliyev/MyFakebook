$(document).ready(function () {
    $('.like').on('click', performClickEvent)
})


var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
        $('.loading').show();
    },

    onAfterPageLoad: function ($items) {
        $('.loading').hide();
        $items.each(function () {
            $(this).find('.like').on('click', performClickEvent);
        })
    }
});