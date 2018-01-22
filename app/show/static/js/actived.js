$(document).ready(function () {
    $('ul.nav-sidebar > li > a[href="' + document.location.pathname + '"]').parent().addClass('active');
    $toggle_sidebar = $('#toggle_sidebar');
    $sidebar = $('.sidebar');
    $main = $('.main');
    $toggle_sidebar.click(function () {
        //$sidebar.toggle();
        if ($sidebar.is(":visible")) {
            $toggle_sidebar.text("显示");
            $sidebar.hide();
            $main.attr("class", "col-sm-12 col-lg-12 main");
        }else {
            $toggle_sidebar.text("隐藏");
            $sidebar.show();
            $main.attr("class", "col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main");
        }
    });
});