(function(){

  var ELASTICSEARCH_INDEX_ENDPOINT = 'http://localhost:9200/around/event/';

  var kms_max = 30;
  var kms_step = 1;
  var kms_radius = 3 * kms_step;

  var max_results = 20;

  var map, centerPt, ctrMarker, searchCircle, radiusSlider;

  var resultTemplate = Handlebars.compile('\
    <tr class="result-row" id={{id}}>\
      <td nowrap="nowrap">\
        {{date_from_human}}{{#if more_days }} - {{date_to_human}}{{/if}}\
        {{#if time_from }}od {{time_from}}{{/if}} {{#if time_to }} do {{time_to}}{{/if}}\
      </td>\
      <td><a href="{{link}}">{{name}}</a></td>\
      <td>{{description}}</td>\
      <td>{{venue}}</td>\
    </tr>\
  ');

  var markers = [];

  google.maps.event.addDomListener(window, 'load', initialize);

  function initialize() {

    $('#max_results').html('(prvnich ' + max_results + ')');

    centerPt = new google.maps.LatLng(49.9262642, 14.2748719);

    var mapOptions = {
      center: centerPt,
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

    var circleOptions = {
      draggable: true,
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      center: centerPt,
      radius: kms_radius * 1000
    };

    searchCircle = new google.maps.Circle(circleOptions);
    
    google.maps.event.addListener(searchCircle, 'mouseup', handleCenterChange);

    var sliderOptions = {
      min: kms_step,
      max: kms_max,
      step: kms_step,
      value: kms_radius,
      orientation: 'horizontal',
      selection: 'after',
      tooltip: 'show',
      handle: 'round',
      formater: formatRadius
    };

    radiusSlider = $('#radius-slider').slider(sliderOptions);
    radiusSlider.on('slideStop', updateRadius);
    radiusSlider.on('slide', circleFeedback);

    radiusSlider.slider('setValue', kms_radius);

    getResults();
  }

  function circleFeedback(e){
    searchCircle.setRadius(e.value * 1000);
  }

  function updateRadius(e) {
    kms_radius = e.value;
    radiusSlider.slider('setValue', kms_radius);
    $('#radius-val').html(formatRadius(kms_radius));
    searchCircle.setRadius(kms_radius * 1000);
    getResults();
  }

  function formatRadius(val) {
    return val + " km";
  }

  function handleCenterChange() {
    var pt = searchCircle.getCenter();
    if (pt != centerPt){
      centerPt = pt;
      getResults();
    }
  }

  function getResults() {
    $('#results').html('');
    markers.map(function(i){
      i.setMap(null);
    });
    markers = [];
    hash = {};
    hash.url = ELASTICSEARCH_INDEX_ENDPOINT + '/_search';
    hash.type = 'POST';
    hash.dataType = 'json';
    hash.success = processResults;
    hash.error = function(arg) { console.error('ajax error: ', arg) };

    hash.data = JSON.stringify({
      "from" : 0,
      "size" : max_results,
      "query" : {
        "filtered" : {
          "query" : { "match_all" : {} },
          "filter" : {
            "geo_distance" : {
                "distance" : (1.00 * kms_radius) + "km",
                "event.coords" : { "lat" : centerPt.lat(), "lon" : centerPt.lng() }
            }
          }
        }
      },
      "sort" : [
        { "date_from" : "asc" },
        { "time_from" : "asc" },
        "_score"
        ],

    });

    jQuery.ajax(hash);
  }

  function processResults(json){
    json['hits']['hits'].map(function(i){
      var src = i['_source'];
      src.id = i["_id"];
      src.more_days = !(src.date_from == src.date_to)
      src.date_from = new Date(src.date_from)
      src.date_to = new Date(src.date_from)
      src.date_from_human = $.formatDateTime('d. m.', src.date_from)
      src.date_to_human = $.formatDateTime('d. m.', src.date_from)
      src.formatted_lat = Math.round(src.coords.lat * 1000000) / 1000000;
      src.formatted_lon = Math.round(src.coords.lon * 1000000) / 1000000;
      $('#results').append(resultTemplate(src));
      var marker = new google.maps.Marker({
        map: map,
        draggable: false,
        position: new google.maps.LatLng(src.coords.lat, src.coords.lon),
        title: [src.first_name, src.last_name].join(' ')
      });
      marker.id = src.id;
      google.maps.event.addListener(marker, 'click', handleMarkerClick);
      markers.push(marker);
    })
  }

  function handleMarkerClick(e){
    $('.result-row').removeClass('alert');
    $('#' + this.id).addClass('alert');
  }


}).call(this);
