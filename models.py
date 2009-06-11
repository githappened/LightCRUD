


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



# add names here to enable _PUBLIC_ access via CRUD
bindings = {
	'Generic': 'Generic',
	'Simple': 'Simple',
	'Complex': 'Complex',
	}



class Generic( db.Model ):
	s = db.StringProperty( default='standalone' )



class Simple( lightcrudmodel.LightCRUDModel ):

	s = db.StringProperty( default='simplicity' )



class Complex( lightcrudmodel.LightCRUDModel ):

	s = db.StringProperty( default='complexity' )
	b = db.BooleanProperty( default=True )
	i = db.IntegerProperty( default=42 )
	f = db.FloatProperty( default=1.618 )
	l = db.ListProperty( str, default=['foo','bar','baz'] )
	u = db.LinkProperty( default='http://example.com/' )
	e = db.EmailProperty( default='example@example.com' )


