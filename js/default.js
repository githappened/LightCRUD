


var thecommons = {};



// FIX: learn how to write modern JavaScript



function alterObjectWithSVGProperties( o, a ) {
	for( var k in a ) {
		o.setAttributeNS( null, k.replace( /_/g, '-' ), a[k] );
	}
}


function makeWithTrivia( t, a ) {
	retval = document.createElementNS( 'http://www.w3.org/2000/svg', t.toLowerCase() );
	alterObjectWithSVGProperties( retval, a );
	return retval;
}


function beginModernBrowsing( ele, modernbrowsernotice ) {
	var commons = thecommons;
	var o = document.createElement( 'div' ); // FIX: learn how to write modern JavaScript
	o.setAttribute( 'width', ele.clientWidth );
	o.setAttribute( 'height', ele.clientHeight );
	commons['widget'] = o;
	commons['svg'] = makeWithTrivia( 'svg:svg', {'width': ele.clientWidth, 'height': ele.clientHeight} );
	o.appendChild( commons['svg'] );
	ele.appendChild( commons['widget'] );
	ele.removeChild( modernbrowsernotice );
	refreshRender();
}


function refreshRender() {
	$.getJSON( '/cRud/.json',
		function( incoming ) { // FIX: learn how to write modern JavaScript
			var commons = thecommons;
			var oldwidget = commons['widget'];
			var svg = makeWithTrivia( 'svg:svg', {'width': oldwidget.clientWidth, 'height': oldwidget.clientHeight} );
			var loopmax = incoming.length;
			for( var loop = 0; loop < loopmax; ++loop ) {
				var kindmax = incoming[loop].length;
				for( var kindloop = 0; kindloop < kindmax; ++kindloop ) {
					var chunk = incoming[loop][kindloop];
					if( chunk ) {
						var t = chunk['kind'];
						chunk['properties']['id'] = t + '_' + chunk['id'];
						svg.appendChild( makeWithTrivia( t.toLowerCase(), chunk['properties'] ) );
					}
				}
			}
			oldwidget.removeChild( commons['svg'] );
			commons['svg'] = svg;
			oldwidget.appendChild( svg );
		});
}


function saveRender() {
	var svg = thecommons['svg']; // FIX: learn how to write modern JavaScript
	if( svg.hasChildNodes() ) {
		var kids = svg.childNodes;
		var loopmax = kids.length;
		for( var loop = 0; loop < loopmax; ++loop ) {
			var kid = kids[loop];
			var id = kid.getAttribute( 'id' );
			var s = id.split( '_' );
			var smax = s.length;
			if( smax >= 2 ) {
				var typename = s[smax - 2];
				var itemid = s[smax - 1];
				var postjs = {};
				var dups = {'id': 'skip'}; // FIX: find a better way
				var kidattr = kid.attributes;
				for( var i in kidattr ) {
					var k = kidattr.item( i ).nodeName
					k = k.replace( /-/g, '_' );
					var v = kidattr.item( i ).value;
					if( ! dups[k] ) { // FIX: find a better way
						postjs[k] = v;
						dups[k] = 42; // FIX: find a better way
					}
				}
				$.post( '/crUd/' + typename + '/' + itemid + '/.json', postjs, null, 'json' );
			}
		}
	}
}


