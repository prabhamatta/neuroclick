$(function () {

        $.get( "/getAverageAttention", function() {
                
                })
                .done(function(data) {
                    categories = []

                    for (var i=1;i<=data.metric1.length;i++){
                        categories.push(i);
                    }

                    $("#users").html("<h2>29</h2>")
                    $("#stimulus").html("<h2>" + data.metric1.length +  "</h2>")


                    $("#avg_val_1").html("<h2>" +data.stats.metric1.mean +"</h2>")
                    $("#min_val_1").html("<h2>" +data.stats.metric1.min +"</h2>")
                    $("#max_val_1").html("<h2>" +data.stats.metric1.max +"</h2>")

                    $("#avg_val_2").html("<h2>" +data.stats.metric2.mean +"</h2>")
                    $("#min_val_2").html("<h2>" +data.stats.metric2.min +"</h2>")
                    $("#max_val_2").html("<h2>" +data.stats.metric2.max +"</h2>")


                    $('#container1').highcharts({

                    chart: {
                        zoomType: 'xy'
                    },
                    title: {
                        text: null,
                        x: -20 //center
                    },
                    exporting:{
                        enabled: false
                    },
                    credits:{
                        enabled:false
                    },
                    
                    xAxis: {
                        categories: categories,
                        tickInterval : 5,
                        plotBands: [{ // mark the weekend
                            color: 'rgba(100, 150, 253, 0.1)',
                            from:0,
                            to: 43
                        }, {
                            color: 'rgba(100, 170, 113, 0.1)',
                            from:43,
                            to:68
                        },{
                            color: 'rgba(40, 100, 113, 0.1)',
                            from:68,
                            to:103
                        }]
                    },
                        tooltip: {
                        formatter: function() {
                            return 'The average value of ' + this.series.name + 'for <b> stimulus'+ this.x +
                                '</b> is <b>'+ this.y +'</b> and it is a <img src="/Users/rahmanaicc/Workspace/Dropbox/BrainDrain/Codebase/neuroclick/neuroclick-app/static/img/pic2.png" />';
                        }
                    },


                    yAxis: {
                        title: {
                            text: 'Attention/Meditation'
                        },
                        min:0,
                        max: 100
//
                    },
                    
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'top',
                        borderWidth: 0
                    },
                    series: [{
                        name: 'Attention',
                        data: data.metric1,
                        color: '#2DA316'
                    },{
                        name: 'Meditation',
                        data: data.metric2,
                        color: '#FE0000'
                    }]
                }); //end of container1


         $('#container2').highcharts({

                    chart: {
                        zoomType: 'xy'
                    },
                    title: {
                        text: null,
                        x: -20 //center
                    },
                    exporting:{
                        enabled: false
                    },
                    credits:{
                        enabled:false
                    },
                    xAxis: {
                        categories: categories,
                        tickInterval : 5,
                        plotBands: [{ // mark the weekend
                            color: 'rgba(100, 150, 253, 0.1)',
                            from:0,
                            to: 43
                        }, {
                            color: 'rgba(100, 170, 113, 0.1)',
                            from:43,
                            to:68
                        },{
                            color: 'rgba(40, 100, 113, 0.1)',
                            from:68,
                            to:103
                        }]
                    },
                        tooltip: {
                        formatter: function() {
                            return 'The average value of ' + this.series.name + 'for <b> stimulus'+ this.x +
                                '</b> is <b>'+ this.y +'</b> and it is a <img src="/Users/rahmanaicc/Workspace/Dropbox/BrainDrain/Codebase/neuroclick/neuroclick-app/static/img/pic2.png" />';
                        }
                    },


                    yAxis: {
                        title: {
                            text: 'Attention/Meditation'
                        },
                        min:0,
                        max: 100
//
                    },
                    
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'top',
                        borderWidth: 0
                    },
                    series: [{
                        name: 'Attention',
                        data: data.metric1,
                        color: '#2DA316'
                    },{
                        name: 'Meditation',
                        data: data.metric2,
                        color: '#FE0000'
                    }]
                }); //end of container2

            });

            $("#analyze").click(function(){
            var user_id = $("#userid").value();
            $.post("/getStatsForUser", function(data){
                console.log(data)
            })

        });
    });
    
