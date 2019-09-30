function liveChartFunction(switchkey) {
    var data = [], totalPoints = 100;

    function getRandomData() {

        if (data.length > 0)
            data = data.slice(1);

        // Do a random walk
        while (data.length < totalPoints) {

            var prev = data.length > 0 ? data[data.length - 1] : 50,
                y = prev + Math.random() * 10 - 5;

            if (y < 0) {
                y = 0
            } else if (y > 100) {
                y = 100
            }

            data.push(y)
        }

        // Zip the generated y values with the x values
        var res = [];
        for (var i = 0; i < data.length; ++i) {
            res.push([i, data[i]])
        }

        return res
    }

    var interactive_plot = $.plot('#interactive', [getRandomData()], {
        grid: {
            borderColor: '#f3f3f3',
            borderWidth: 1,
            tickColor: '#f3f3f3'
        },
        series: {
            shadowSize: 0, // Drawing is faster without shadows
            color: '#28c76f'
        },
        lines: {
            fill: true, //Converts the line chart to area chart
            color: '#28c76f'
        },
        yaxis: {
            min: 0,
            max: 100,
            show: true
        },
        xaxis: {
            show: true
        }
    });

    var updateInterval = 500; //Fetch data ever x milliseconds
    var realtime = switchkey; //If == to on then fetch data every x seconds. else stop fetching
    function update() {

        interactive_plot.setData([getRandomData()]);

        // Since the axes don't change, we don't need to call plot.setupGrid()
        interactive_plot.draw();
        if (realtime === 'on')
            setTimeout(update, updateInterval)
    }

    //INITIALIZE REALTIME DATA FETCHING
    if (realtime === 'on') {
        update()
    }

    var sin = [], cos = [];
    for (var i = 0; i < 14; i += 0.5) {
        sin.push([i, Math.sin(i)]);
        cos.push([i, Math.cos(i)])
    }
    var line_data1 = {
        data: sin,
        color: '#3c8dbc'
    };
    var line_data2 = {
        data: cos,
        color: '#00c0ef'
    };
    $.plot('#line-chart', [line_data1, line_data2], {
        grid: {
            hoverable: true,
            borderColor: '#f3f3f3',
            borderWidth: 1,
            tickColor: '#f3f3f3'
        },
        series: {
            shadowSize: 0,
            lines: {
                show: true
            },
            points: {
                show: true
            }
        },
        lines: {
            fill: false,
            color: ['#3c8dbc', '#f56954']
        },
        yaxis: {
            show: true
        },
        xaxis: {
            show: true
        }
    });
    //Initialize tooltip on hover
    $('<div class="tooltip-inner" id="line-chart-tooltip"></div>').css({
        position: 'absolute',
        display: 'none',
        opacity: 0.8
    }).appendTo('body');
    $('#line-chart').bind('plothover', function (event, pos, item) {

        if (item) {
            var x = item.datapoint[0].toFixed(2),
                y = item.datapoint[1].toFixed(2);

            $('#line-chart-tooltip').html(item.series.label + ' of ' + x + ' = ' + y)
                .css({top: item.pageY + 5, left: item.pageX + 5})
                .fadeIn(200)
        } else {
            $('#line-chart-tooltip').hide()
        }

    });
    /* END LINE CHART */

    /*
     * FULL WIDTH STATIC AREA CHART
     * -----------------
     */
    var areaData = [[2, 88.0], [3, 93.3], [4, 102.0], [5, 108.5], [6, 115.7], [7, 115.6],
        [8, 124.6], [9, 130.3], [10, 134.3], [11, 141.4], [12, 146.5], [13, 151.7], [14, 159.9],
        [15, 165.4], [16, 167.8], [17, 168.7], [18, 169.5], [19, 168.0]];
    $.plot('#area-chart', [areaData], {
        grid: {
            borderWidth: 0
        },
        series: {
            shadowSize: 0, // Drawing is faster without shadows
            color: '#00c0ef'
        },
        lines: {
            fill: true //Converts the line chart to area chart
        },
        yaxis: {
            show: false
        },
        xaxis: {
            show: false
        }
    });

    /* END AREA CHART */

}

var workerInterval = null;

$('#workerBotStartButton').click(
    function () {
        let tempurl = window.location.protocol + "//" + window.location.host + "/bots/worker/";
        var tempData = function () {
           var variable  = {'empty':'empty'}

            var tmp = null;
            $.ajax({
                'async': false,
                'type': "GET",
                'global': false,
                'dataType': 'json',
                'data': JSON.stringify(variable),
                'contentType': 'application/json; charset=utf-8',
                'url': tempurl,
                'success': function (data) {
                    tmp = data;
                }
            });
            return tmp;
        }();

        console.log(tempData.task_id);

        $('#interactive').empty();

        workerInterval = setInterval(LoadLiveWorkerBotStatus, 5000, tempData.task_id)

        lgraph = liveChartFunction('off');


        $("#worker_bot-runbutton-msg").text("Running").css("color", "#28c76f");
    });
var nidInterval = null;

$('#nidBotStartButton').click(
    function () {

        let tempurl = window.location.protocol + "//" + window.location.host + "/bots/nid/";
        var tempData = function () {
            var tmp = null;
            $.ajax({
                'async': false,
                'type': "GET",
                'global': false,
                'dataType': 'json',
                'contentType': 'application/json; charset=utf-8',
                'url': tempurl,
                'success': function (data) {
                    tmp = data;
                }
            });
            return tmp;
        }();

        console.log(tempData.task_id);

        nidInterval = setInterval(LoadLiveNidBotStatus, 5000, tempData.task_id)



        $('#interactive').empty();

        lgraph = liveChartFunction('on');


        $("#nid_bot-runbutton-msg").text("Running").css("color", "#28c76f");

    });

function LoadLiveStatus() {
        let tempurl = window.location.protocol + "//" + window.location.host + "/bots/status/";
        var tempData = function () {
            var tmp = null;
            $.ajax({
                'async': false,
                'type': "GET",
                'global': false,
                'dataType': 'json',
                'contentType': 'application/json; charset=utf-8',
                'url': tempurl,
                'success': function (data) {
                    tmp = data;
                }
            });
            return tmp;
        }();

        console.log(tempData.process_count);

        $('#process-completed-number').text(tempData['process_count']);
        $('#success-percentage-number').text(tempData['percentage'] + "%");

}
function LoadLiveNidBotStatus(t_id) {
        let tempurl = "/bots/process-status-nid/"+t_id+"/";

        var sendSomething = function () {

            var tmp = null;
            $.ajax({
                'async': false,
                'type': "GET",
                'global': false,
                'dataType': 'json',
                'contentType': 'application/json; charset=utf-8',
                'url': tempurl,
                'success': function (data) {
                    tmp = data;
                }
            });
            return tmp;
        }();
        console.log(sendSomething);

        if (sendSomething.status == true) {
            clearInterval(nidInterval)
        }

}

function LoadLiveWorkerBotStatus(t_id) {
        let tempurl = "/bots/process-status-worker/"+t_id+"/";

        var sendSomething = function () {

            var tmp = null;
            $.ajax({
                'async': false,
                'type': "GET",
                'global': false,
                'dataType': 'json',
                'contentType': 'application/json; charset=utf-8',
                'url': tempurl,
                'success': function (data) {
                    tmp = data;
                }
            });
            return tmp;
        }();
        console.log(sendSomething);

        if (sendSomething.status == true) {
            clearInterval(workerInterval)
        }

}

LoadLiveStatus();
setInterval(LoadLiveStatus, 10000);

function startConnection() {
    console.log("starting the communication channel");
    client = new Paho.MQTT.Client('103.108.140.185', Number(8080), '', '');

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // connect the client
    client.connect({onSuccess: onConnect});


    // called when the client connects
    function onConnect() {
        // Once a connection has been made, make a subscription and send a message.
        console.log("onConnect");
        client.subscribe("aiw");
        message = new Paho.MQTT.Message("");
        message.destinationName = "aiw";
        client.send(message);
    }

    // called when the client loses its connection
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }
    }

    // called when a message arrives
    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);

        $('#server-feed').prepend(message.payloadString);

    }
}

startConnection();
