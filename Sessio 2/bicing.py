#!/usr/bin/python
import urllib
import xml.etree.ElementTree as ET

sock = urllib.urlopen("http://wservice.viabicing.cat/getstations.php?v=1")
xmlSource = sock.read()
sock.close()

# print xmlSource

root = ET.fromstring(xmlSource)

print '<!DOCTYPE HTML SYSTEM>'
print '<html lang="es">'
print '<head>'
print '    <meta http-equiv="Content-Type">'
print '    <meta http-equiv="X-UA-Compatible" content="IE=edge">'
print '    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
print '    <meta http-equiv="Window-target" content="_top" >'
print '    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">'
print '    <title>BICING</title>'
print ' <script type="text/javascript">'
print 'function initialize() {'
print 'var mapOptions = {'
print '          zoom: 14,'
print '          center: new google.maps.LatLng(41.3933466, 2.147914),'
print '          mapTypeControlOptions: {'
print '            mapTypeIds: [google.maps.MapTypeId.ROADMAP, MYMAP]'
print '          },'
print '          mapTypeId: MYMAP'
print '        };'
print '        var map = new google.maps.Map(document.getElementById(''map-canvas''), mapOptions);'
print ''
print 'var customMapType = new google.maps.StyledMapType(featureOpts, styledMapOptions);'
print '        map.mapTypes.set(MYMAP, customMapType);'
print ''
print '        setMarkers(map);'
print '      }'

print'      function setMarkers(map) {'
cont = 0
for estacio in root.findall('station'):
	cont = cont + 1
	slots = int(estacio.find('slots').text)
	bikes = int(estacio.find('bikes').text)
	carrer = estacio.find('street').text
	numeroCarrer = estacio.find('streetNumber').text
	if slots > 2:
		if bikes > 2:
			descripcio = carrer, ' ', numeroCarrer, '\n', 'places lliures: ', slots, '\n', 'bicis disponibles: ', bikes
			print 'var contentString'+str(cont), '=', descripcio,';'
	        print 'var infowindow'+str(cont), '= new google.maps.InfoWindow({'
	        print 'content: contentString'+str(cont)
	        print '});'
	        print 'var myLatLng'+str(cont), '= new google.maps.LatLng(',estacio.find('lat').text, estacio.find('long').text,');'
	        print 'var marker'+str(cont), '= new google.maps.Marker({'
	        print 'position: myLatLng'+str(cont),','
	        print 'map: map,'
	        print 'title:'+str(cont)
	        print '});'
	        print 'google.maps.event.addListener(marker'+str(cont) ,', ''click'', function() {'
	        print 'infowindow'+str(cont),'.open(map, marker'+str(cont),');'
	        print '}'

print      'google.maps.event.addDomListener(window, ''load'', initialize);'
print '   </script> </head>'
print '<body>'
print '<div id="map-canvas"></div>'
print '</body>'
