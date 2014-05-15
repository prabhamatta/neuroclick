/**
 * Created by rahmanaicc on 5/8/14.
 */
$(function () {


    $.get( "/getTextStats", function() {

    })
        .done(function(data) {
            categories = ['Long Text', 'Short Text']

            val_arr = []
            val_arr.push(data.stats.long.mean)
            val_arr.push(data.stats.short.mean)
            $('#blink-data-container-text').highcharts({

                chart: {
                    zoomType: 'xy',
                    type: 'bar'
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

                },
                tooltip: {
                    formatter: function() {
                        return 'The average value of ' + this.series.name + 'for <b> stimulus'+ this.x +
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Beta'
                    }
//                    min:25,
//                    max: 75
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Beta',
                    data: val_arr,
                    color: '#2DA316'
                }
//                    ,{
//                    name: 'High Alpha',
//                    data: data.metric2,
//                    color: '#FE0000'
//                }
                ]
            }); //end of container1




        });


    $.get( "/getVideoStats", function() {

    })
        .done(function(data) {
            categories = ['Long Video', 'Short Video']

            val_arr = []
            val_arr.push(data.stats.long.mean)
            val_arr.push(data.stats.short.mean)
            $('#blink-data-container-video').highcharts({

                chart: {
                    zoomType: 'xy',
                    type: 'bar'
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
                    categories: categories

                },
                tooltip: {
                    formatter: function() {
                        return 'The average value of ' + this.series.name + 'for <b> stimulus'+ this.x +
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Beta'
                    }
//                    min:25,
//                    max: 75
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Beta',
                    data: val_arr,
                    color: '#2DA316'
                }
//                    ,{
//                    name: 'High Alpha',
//                    data: data.metric2,
//                    color: '#FE0000'
//                }
                ]
            }); //end of container1




        });






    $.get( "/getAverageAlpha", function() {

    })
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-alpha').highcharts({

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
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Alpha'
                    }
//                    min:25,
//                    max: 75
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Alpha',
                    data: data.average,
                    color: '#2DA316'
                }
//                    ,{
//                    name: 'High Alpha',
//                    data: data.metric2,
//                    color: '#FE0000'
//                }
                ]
            }); //end of container1




        });


    $.get( "/getGenderAlpha", function() {

    })
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-alpha-gender').highcharts({

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
                    plotBands: [{
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
                        return 'The average value of alpha for ' + this.series.name + 'for <b> stimulus'+ this.x +
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Male/Female'
                    }
//                    min:0,
//                    max: 100
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Female',
                    data: data.metric2,
                    color: 'rgba(255, 105, 180, 0.9)'
                },{
                    name: 'Male',
                    data: data.metric1,
                    color: 'rgba(50, 50, 250, 0.6)'
                }]
            }); //end of container1

        });




    $.get( "/getAverageBeta", function() {})
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-beta').highcharts({

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
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Beta '
                    }
//                    min:25,
//                    max: 75
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Beta',
                    data: data.average,
                    color: '#2DA316'
                }
//                    ,{
//                    name: 'High Beta',
//                    data: [],
//                    color: '#FE0000'
//                }
                ]
            }); //end of container2

        });

     $.get( "/getGenderBeta", function() {

    })
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-beta-gender').highcharts({

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
                    plotBands: [{
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
                        return 'The average value of beta for ' + this.series.name + 'for <b> stimulus'+ this.x +
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Male/Female'
                    }
//                    min:0,
//                    max: 100
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Female',
                    data: data.metric2,
                    color: 'rgba(255, 105, 180, 0.9)'
                },{
                    name: 'Male',
                    data: data.metric1,
                    color: 'rgba(50, 50, 250, 0.6)'
                }]
            }); //end of container1

        });


    $.get( "/getAverageGamma", function() {

    })
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-gamma').highcharts({

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
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Gamma'
                    }
//                    min:25,
//                    max: 75
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Gamma',
                    data: data.average,
                    color: '#2DA316'
                }
//                    ,{
//                    name: 'Mid Gamma',
//                    data: data.metric2,
//                    color: '#FE0000'
//                }
                ]
            }); //end of container3

        });

     $.get( "/getGenderGamma", function() {

    })
        .done(function(data) {
            categories = []

            for (var i=1;i<=data.metric1.length;i++){
                categories.push(i);
            }

            $('#blink-data-container-gamma-gender').highcharts({

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
                    plotBands: [{
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
                        return 'The average value of gamma for ' + this.series.name + 'for <b> stimulus'+ this.x +
                            '</b> is <b>'+ this.y +'</b>';
                    },
                    borderWidth: 0

                },


                yAxis: {
                    title: {
                        text: 'Male/Female'
                    }
//                    min:0,
//                    max: 100
//
                },

                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'top',
                    borderWidth: 0
                },
                series: [{
                    name: 'Female',
                    data: data.metric2,
                    color: 'rgba(255, 105, 180, 0.9)'
                },{
                    name: 'Male',
                    data: data.metric1,
                    color: 'rgba(50, 50, 250, 0.6)'
                }]
            }); //end of container1

        });









});

