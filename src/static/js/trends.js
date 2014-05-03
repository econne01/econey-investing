/**
 * Create a timeline chart to show the recent high and low price dates
 * for the given price trend data
 *
 */
var createTrendTimelineChart = function(ticker, data, timeScale) {
    var width = 450,
        height = 60;

    var dates = [
        { date: data.min_price_date, price: data.min_price },
        { date: data.max_price_date, price: data.max_price }
    ];
    var min_date, max_date;
    if (data.min_price_date <= data.max_price_date) {
        min_date = data.min_price_date;
        max_date = data.max_price_date;
    } else {
        max_date = data.min_price_date;
        min_date = data.max_price_date;
    };

    var parseDate = d3.time.format('%Y-%m-%d').parse;

    if (typeof timeScale === 'undefined') {
        timeScale = d3.time.scale()
            .domain([parseDate('2014-03-15'), parseDate('2014-05-15')])
            .range([0,width]);
    };

    var yScale = d3.scale.linear()
        .domain([0, 30])
        .range([height, 0]);

    var xAxis = d3.svg.axis().scale(timeScale).orient('bottom');
    var yAxis = d3.svg.axis().scale(yScale).orient('left');

    var line = d3.svg.line()
        .x(function(dataPoint, index) {
            return timeScale(parseDate(dataPoint.date));
        })
        .y(function(dataPoint, index) { return 10; });

    var svg = d3.select('tr#' + ticker + ' td.chart-trend').append('svg')
        .attr('width', width)
        .attr('height', height);

    svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(50,30)')
        .call(xAxis);

    svg.append('path').attr('d', line(dates));
};


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

    var timeScale = d3.time.scale()
        .domain([parseDate('2014-03-15'), parseDate('2014-05-15')])
        .range([0, 450]);
    var xAxis = d3.svg.axis().scale(timeScale).orient('bottom');

    var chartColumnHeader = d3.select('th#chart-trend-header').append('svg');
    chartColumnHeader.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(50,30)')
        .call(xAxis);

    $.getJSON($SCRIPT_ROOT + '/api/trends', {
        tickers: tickers.join(',')
    }, function(data) {
        for (var i=0; i < data.trends.length; i++) {
            var row = data.trends[i];
            var chartTd = $('#' + row.ticker).find('td.chart-trend')[0];

            createTrendTimelineChart(row.ticker, row, timeScale);
        };
    });
    return false;
});
