var data = [{"count": 1, "proto": "arp"}, {"count": 6, "proto": "tcp"}]

var chart = d3.select("body").append("div")
    .attr("class", "chart");
    
chart.selectAll("div")
    .data(data)
    .enter()
    .append("div")
    .style("width", function(d) { return d.count * 10 + "px"; })
    .text(function(d) { return d; });
    

