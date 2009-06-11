


# Copyright 2009 Gary Johnson

# This file is part of LightCRUD.
#
# LightCRUD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LightCRUD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LightCRUD.  If not, see <http://www.gnu.org/licenses/>.



from google.appengine.ext import db


import lightcrudmodel


import sys



# add names here to enable _PUBLIC_ access via CRUD
bindings = {
	'Line': 'Line',
	'Circle': 'Circle',
	'Rect': 'Rect',
	}



def make_kind_of_model_by_name( name ):
	retval = None
	if name and name in bindings.keys():
		retval = getattr( sys.modules[__name__], bindings[name] )
	return retval



class CatchAll( db.Model ):

	stroke = db.StringProperty( default='black' )
	stroke_opacity = db.FloatProperty( default=0.42 )
	stroke_width = db.StringProperty( default='3' )
	onmousedown = db.StringProperty( default='' ) # FIX: db.TextProperty()?
	onmousemove = db.StringProperty( default='' ) # FIX: db.TextProperty()?
	onmouseup = db.StringProperty( default='' ) # FIX: db.TextProperty()?
	onclick = db.StringProperty( default='' ) # FIX: db.TextProperty()?



class Line( CatchAll ):

	x1 = db.StringProperty( default='1' )
	y1 = db.StringProperty( default='1' )
	x2 = db.StringProperty( default='42' )
	y2 = db.StringProperty( default='42' )



class Circle( CatchAll ):

	cx = db.StringProperty( default='42' )
	cy = db.StringProperty( default='42' )
	r = db.StringProperty( default='42' )
	fill = db.StringProperty( default='black' )
	fill_opacity = db.FloatProperty( default=0.42 )



class Rect( CatchAll ):

	x = db.StringProperty( default='1' )
	y = db.StringProperty( default='1' )
	width = db.StringProperty( default='56' )
	height = db.StringProperty( default='56' )
	rx = db.StringProperty( default='0' )
	ry = db.StringProperty( default='0' )
	fill = db.StringProperty( default='black' )
	fill_opacity = db.FloatProperty( default=0.1618 )


