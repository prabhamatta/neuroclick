var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = 4000 - margin.left - margin.right,
    height = 390 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y%m%d").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.Time); })
    .y(function(d) { return y(d.signal); });

var svg = d3.select("#metrics").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

$('#heading').empty();
$('#heading').append(" Attention Chart");

d3.csv("data/attention.csv", function(error, data) {
  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Time"; }));

  data.forEach(function(d) {
    // d.Time = parseDate(d.Time);
    var tim = new Date();             
    tim.setHours(d.Time.split(":")[0]);
    tim.setMinutes(d.Time.split(":")[1]);
    tim.setSeconds(d.Time.split(":")[2]); 
    d.Time = tim;
  });

  var cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {Time: d.Time, signal: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.Time; }));

  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.signal; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.signal; }); })
  ]);

    //   //xAxisGridLines and yAxisGridLines for the grid lines        
    // var xAxisGridLines = d3.svg.axis()
    //                         .scale(xAxis)
    //                         .orient("bottom")
    //                         .ticks(20);

    // var yAxisGridLines = d3.svg.axis()
    //                         .scale(yAxis)
    //                         .orient("left")
    //                         .ticks(10);


  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("signal ");

    // //Drawing Grid Lines
    // var xGridLines = svg.append("g")
    //                     .attr("class", "grid")
    //                     .attr("transform", "translate(" + 40 + "," + (height - 20)  + ")")
    //                     .style("stroke-dasharray", ("3, 3"))
    //                     .call(xAxisGridLines
    //                         .tickSize(-height + 30,0,0)
    //                         .tickFormat("")


    //                     );
                                                            
    // var yGridLines = svg.append("g")
    //                     .attr("class", "grid")
    //                     .attr("transform", "translate(40,10)")
    //                     .style("stroke-dasharray", ("3, 3"))
    //                     .call(yAxisGridLines
    //                         .tickSize(-width + 40,0,0)
    //                         .tickFormat("")

    //                     );
  var city = svg.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.Time) + "," + y(d.value.signal) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });
});