


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


from django.utils import simplejson



def toJSON( d ):
	return simplejson.dumps( d )


def fromJSON( j ):
	return simplejson.loads( j )



class LightCRUDModel( db.Model ):

	created = db.DateTimeProperty( auto_now_add=True )
	revised = db.DateTimeProperty( auto_now=True )


	def apply_dict( self, d ):
		if self.properties() and d:
			p = self.properties()
			if p and p.has_key( 'properties' ):
				p = p['properties']
			propertynames = [propertyname for propertyname in p if propertyname not in ignorables and propertyname in d]
			for propertyname in propertynames:
				T = type( getattr( self, propertyname ) ) # yes, types, there is no escape
				setattr( self, propertyname, (T)(d[propertyname]) ) # trigger the Property.validate() check


	def extract_dict( self ):
		retval = {'id': self.key().id_or_name(), 'kind': self.kind()}
		if self.properties():
			retval['properties'] = {}
			propertynames = [propertyname for propertyname in self.properties() if propertyname not in ignorables]
			for propertyname in propertynames:
				retval['properties'][propertyname] = getattr( self, propertyname )
		return retval


	def toJSON( self ):
		return toJSON( self.extract_dict() )


	def fromJSON( self, d ):
		self.apply_dict( fromJSON.loads( d ) )



# filter out read/write of these values (via dicts)
ignorables = [key for key in LightCRUDModel.properties().keys() if LightCRUDModel.properties()]


