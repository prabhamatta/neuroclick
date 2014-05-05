var data;
var state_data; // loaded asynchronously
var county_data;
var counties_paths;
var path = d3.geo.path();
var zoomed = false;

var disp = true;

var svg = d3.select("#chart")
    .append("svg")
    // .call(d3.behavior.zoom()
    //     .on("zoom", redraw))

var g = svg.append("g")

var counties = g.append("g")
    .attr("id", "counties")
    .attr("class", "Purples");

var states = g.append("g")
    .attr("id", "states")
    .attr("class", "Purples");

var tooltip = d3.select("body")
    .append("div")
    .attr("id", "tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")

d3.json("static/json/us-counties.json", function(json) {
    counties_paths = json.features;
    counties.selectAll("path")
        .data(json.features)
        .enter().append("path")
        // .attr("class", (county_data & cd) ? cquantize : null)
        // .on("mouseover", function(d){cmapover(d, this)})
        .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
        .on("click", function(d) {hidecounties (d, this)})
        .on("mouseout", function(){
            d3.select(this)
                .style('stroke', "#fff")
                .style('stroke-width', '.25px')
            return tooltip.style("visibility", "hidden");})
        .attr("d", path);
});

d3.json("static/json/us-states.json", function(json) {

    states.selectAll("path")
        .data(json.features)
        .enter().append("path")
        // .attr("class", (state_data & cd) ? quantize : null)
        // .on("mouseover", function(d){mapover(d, this)})
        .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
        .on("click", function (d) {showcounties(d, this)})
        .attr("d", path)
        .on("mouseout", function(){
            d3.select(this)
                .style('stroke', "#77f")
                .style('stroke-width', '1.5px')
            return tooltip.style("visibility", "hidden");})
        .attr("d", path);

});

d3.json("static/json/unemployment.json", function(json) {
   data = json;
   counties.selectAll("path")
       .attr("class", quantize);
 });
function quantize(d) {
   return "q" + Math.min(8, ~~(data[d.id] * 9 / 12)) + "-9";
 }


// var currday = 0
// var cd

// $('#search-btn').on('click', function(e){
//     band = $("#search").val()

//     d3.json("statecount?query=" + band, function (json) {
//         data = json
//         json.forEach(function(d) {
//             d.date = parse(d[0])
//             d.count = d[1]
//             d.pct = d[2]
//             d.states = d[3]
//         })
//         cd = json[0][0]
//         state_data = json[0].states
//         states.selectAll("path")
//             .attr("class", state_data ? quantize : null)
//         counties.selectAll("path")
//             .attr("class", county_data ? cquantize : null)
//         x.domain([json[0].date, json[json.length - 1].date]);
//         y.domain([0, d3.max(json, function(d) { return d.count; })]).nice();
        

//         tsvg.append("svg:clipPath")
//             .attr("id", "clip")
//             .append("svg:rect")
//             .attr("width", w)
//             .attr("height", h);

//         areapath.attr("d", area(json));

//         xaxispath.attr("transform", "translate(0," + h + ")")
//             .call(xAxis);

//         yaxispath.call(yAxis);  

//         linepath.attr("d", line(json));

//         textanchor.text("Talks");
        
//         tsvg.selectAll(".dot").remove('circle')
//         tsvg.selectAll(".dot")
//             .data(json)
//             .enter().append("circle")
//             .attr("class", "dot")
//             .attr("r", 4)
//             .attr("cx", function(d) { return x(d.date); })
//             .attr("cy", function(d) { return y(d.count); })
//             .on("mouseover", function(d){changetime(d, this)})
//             .on("mousemove", function(){return ttooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})   
//             .on("mouseout", function(d){
//                     ttooltip.style("visibility", "hidden")
//                     d3.select(this).attr('r', 4)
//                 })
//                 // .style("fill", function(d) { return color(d.species); });
//     })
// })


// function quantize(d) {
//     var state = state_data[d.id]
//     if (state) {
//         var total = 0
//         var count = 0
//         var pct = 0.0
//         for (var s in state_data) {
//             count += 1
//             total += state_data[s][2]
//             pct += state_data[s][1]
//         }
//         if (disp)
//             return "q" + Math.min(8, ~~(state[2]/total * count*4)) + "-9";
//         else {
//             return "q" + Math.min(8, ~~(state[1]/pct * count*4)) + "-9";
//         }
            
//     }
//     return 'q0-9'
// }

// function cquantize(d) {
//     var county = county_data[d.id]
//     if (county) {
//         var total = 0
//         var count = 0
//         var pct = 0.0
//         for (var s in county_data) {
//             count += 1
//             total += county_data[s][2]
//             pct += county_data[s][1]
//         }
//         if (disp)
//             return "q" + Math.min(8, ~~(county[2]/total * count*4)) + "-9";
//         else {
//             return "q" + Math.min(8, ~~(county[1]/pct * count*4)) + "-9";
//         }
//     }
//     return 'q0-9'
// }

// function mapover(d, self){
//     d3.select(self)
//         .style('stroke', "#000")
//         .style('stroke-width', "3px")
//     var state = state_data[d.id]
//     var tooltext = "County: "+d.properties.name+", Tweet Count: 0; Tweet Pct: 0%"
//     if (state) {
//         tooltext = "County: "+d.properties.name+", Tweet Count: "+ state[2] +
//                     "; Tweet Pct: " + Number(state[1].toFixed(2) * 100) + "%"
//     }
//     tooltip.text(tooltext)
//         .style("visibility", "visible");
// };

// // Function when user hovers county in the map
// function cmapover(d, self){
//     d3.select(self)
//         .style('stroke', "#000")
//         .style('stroke-width', "2px")
//     var county = county_data[d.id]
//     var tooltext = "County: "+d.properties.name+", Tweet Count: 0; Tweet Pct: 0%"
//     if (county) {
//         tooltext = "County: "+d.properties.name+", Tweet Count: "+ county[2] +
//                     "; Tweet Pct: " + Number((county[1] * 100).toFixed(2)) + "%"
//     }
//     tooltip.text(tooltext)
//         .style("visibility", "visible");
// };



function showcounties (d, self) {
    zoomed = true;
    var centroid = path.centroid(d)
    console.log(centroid)
    d3.select(self).style("visibility", "hidden")
    d3.json("countycount?band=" + band + "&state=" + d.id, function (json) {
        json.forEach(function(d) {
            d.date = parse(d[0])
            d.count = d[1]
            d.pct = d[2]
            d.counties = d[3]
        })

        county_data = json[0].counties
        counties.selectAll("path")
                .attr("class", county_data ? cquantize : null)

        x.domain([json[0].date, json[json.length - 1].date]);
        y.domain([0, d3.max(json, function(d) { return d.count; })]).nice();
        

        tsvg.append("svg:clipPath")
            .attr("id", "clip")
            .append("svg:rect")
            .attr("width", w)
            .attr("height", h);

        areapath.attr("d", area(json));

        xaxispath.attr("transform", "translate(0," + h + ")")
            .call(xAxis);

        yaxispath.call(yAxis);  

        linepath.attr("d", line(json));

        textanchor.text("Talks");
        
        tsvg.selectAll(".dot").remove('circle')
        tsvg.selectAll(".dot")
            .data(json)
            .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 4)
            .attr("cx", function(d) { return x(d.date); })
            .attr("cy", function(d) { return y(d.count); })
            .on("mouseover", function(d){changetime(d, this)})
            .on("mousemove", function(){return ttooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})   
            .on("mouseout", function(d){
                    ttooltip.style("visibility", "hidden")
                    d3.select(this).attr('r', 4)
                })
    })
    g.transition()
        .duration(1000)
        .attr("transform", "scale(" + 2 + ")translate(" + (-centroid[0]+200) + "," + (-centroid[1]+100) + ")")
}

function hidecounties (d, self) {
    zoomed = false;
    console.log("hiding")
    states.selectAll("path")
        .style("visibility", "visible")
    g.transition()
        .duration(1000)
        .attr("transform", "scale(" + 1 + ")translate(" + 0 + "," + 0 + ")")
    x.domain([data[0].date, data[data.length - 1].date]);
    y.domain([0, d3.max(data, function(d) { return d.count; })]).nice();
        

    tsvg.append("svg:clipPath")
        .attr("id", "clip")
        .append("svg:rect")
        .attr("width", w)
        .attr("height", h);

    areapath.attr("d", area(data));

    xaxispath.attr("transform", "translate(0," + h + ")")
        .call(xAxis);

    yaxispath.call(yAxis);  

    linepath.attr("d", line(data));

    textanchor.text("Talks");
    
    tsvg.selectAll(".dot").remove('circle')
    tsvg.selectAll(".dot")
        .data(data)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("r", 4)
        .attr("cx", function(d) { return x(d.date); })
        .attr("cy", function(d) { return y(d.count); })
        .on("mouseover", function(d){changetime(d, this)})
        .on("mousemove", function(){return ttooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})   
        .on("mouseout", function(d){
                ttooltip.style("visibility", "hidden")
                d3.select(this).attr('r', 4)
            })

}

function renderMap(d, self) {
    if (!zoomed) {
        states.selectAll("path")
            .attr("class", quantize);
    } else {
        counties.selectAll("path")
            .attr("class", cquantize);
    }

}

$('#count').on('click', function(e){
    $("#count").toggleClass('active')
    $("#pct").toggleClass('active')
    disp = true
    renderMap();
})

$('#pct').on('click', function(e){
    $("#count").toggleClass('active')
    $("#pct").toggleClass('active')
    disp = false
    renderMap();
})



