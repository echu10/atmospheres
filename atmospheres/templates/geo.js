var app = angular.module('app', [])

.directive('mapViz', function() {

    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
var width = 600,
    height = 400,
    div = d3.select('body')
        .append('div')
        .attr('id','map')
        .style('width', width + 'px')
        .style('height', height + 'px');
            
// Create the Google Map…
var map = new google.maps.Map(div.node(), {
  zoom: 12,
  center: new google.maps.LatLng(37.76487, -122.41948),
  mapTypeId: google.maps.MapTypeId.TERRAIN,
  minZoom: 2  // stuff goes wrong if we allow world wraparound
});


          
// Load the  data. When the data comes back, create an overlay.
queue()
    .defer(d3.json, "{{ url_for('static', filename='sf_zips.topo.json') }}")
    .await(ready)

var svg, overlay;

function ready(error, world) {
    var zipcodes = topojson.feature(world, world.objects.geo).features,  
        // land = topojson.feature(world, world.objects.land);

    overlay = new google.maps.OverlayView();
    overlay.onAdd = function() {
        // create an SVG over top of it. 
        svg = d3.select(overlay.getPanes().overlayLayer)
            .append('div')
                .attr('id','d3map')
                .style('width', width + 'px')
                .style('height', height + 'px')
            .append('svg')
                .attr('width', width)
                .attr('height', height);
            
        svg.append('g')
            .attr('id','zipcodes')
            .selectAll('path')
                .data(zipcodes)
              .enter().append('path')
                .attr('class','zipcode')
                .attr("id",function(d){return "zip_"+d.id})
        
        overlay.draw = redraw;
        google.maps.event.addListener(map, 'bounds_changed', redraw);
        google.maps.event.addListener(map, 'center_changed', redraw);
    };
    overlay.setMap(map);

    //this is a hack!
    setTimeout(updateColors, 100)
}

function updateColors()
{
    d3.select("#zip_94105")
        .style('fill', 'red');

    d3.select("#zip_94111")
        .style('fill', 'aquamarine');

    d3.select("#zip_94132")
        .style('fill', 'purple');

}

function redraw() {
    
    var bounds = map.getBounds(),
        ne = bounds.getNorthEast(),
        sw = bounds.getSouthWest(),
        projection = d3.geo.mercator()
            .rotate([-bounds.getCenter().lng(),0])
            .translate([0,0])
            //.center([0,0])
            .scale(1),
        path = d3.geo.path()
            .projection(projection);
            
    var p1 = projection([ne.lng(),ne.lat()]),
        p2 = projection([sw.lng(),sw.lat()]);
    
    svg.select('#zipcodes').attr('transform', 
        'scale('+width/(p1[0]-p2[0])+','+height/(p2[1]-p1[1])+')'+
        'translate('+(-p2[0])+','+(-p1[1])+') ');
              
    svg.selectAll('path').attr('d', path);
    }
        }
    };
});