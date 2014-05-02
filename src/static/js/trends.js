/**
 * Run on load to get the Trend data (recent price ranges)
 * for a list of tickers
 *
 */
$(function() {
    var tickers = [
        'AXP',
        'BA'
    ];

    $.getJSON($SCRIPT_ROOT + '/api/trends', {
        tickers: tickers.join(',')
    }, function(data) {
        console.log(data);
    });
    return false;
});
