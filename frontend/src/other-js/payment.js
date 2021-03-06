$(function () {
    function getParameterByName(name, url) {
        if (!url) url = window.location.href;
        name = name.replace(/[\[\]]/g, "\\$&");
        var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, " "));
    }

    function setAmount(amount) {
        console.log("AMOUNT:", amount)
        $(".amount").text(parseFloat(amount).toFixed(2))
    }

    var sessionAmount = JSON.parse(sessionStorage.getItem("amount"));
    var urlAmount = getParameterByName('amount')
    if (urlAmount != null) {
        setAmount(urlAmount)
    }

    if(sessionAmount != null) {
        setAmount(sessionAmount)
    }

    $('[data-toggle="popover"]').popover();

    $('#cvc').on('click', function () {
        if ($('.cvc-preview-container').hasClass('hide')) {
            $('.cvc-preview-container').removeClass('hide');
        } else {
            $('.cvc-preview-container').addClass('hide');
        }
    });

    $('.cvc-preview-container').on('click', function () {
        $(this).addClass('hide');
    });

    $("#PayButton").click(function () {
        $("#PayButton").attr('disabled', true)
        $("#PayButton i").show()
        window.setTimeout(
            function() {
                window.location.href = '/success.html'
            },
            2000
        )
    })

});