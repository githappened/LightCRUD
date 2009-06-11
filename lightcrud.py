


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



from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app


import lightcrudmodel
import models


import re



# FIX: refactor the following tedium, all of it



class CrudHandler( webapp.RequestHandler ):


	def get( self ):
		self.post()


	def post( self ):
		self.response.out.write( 'Bummer, your request reached this code stub.' )


	def get_REST_path( self ):
		return [piece for piece in self.request.path.split( '/' ) if piece]


	def get_REST_dict( self ):
		retval = {}
		for name in self.request.arguments():
			if name and self.request.get( name ):
				retval[name] = self.request.get( name )
		return retval


	def get_REST_CRUD_index( self ): # FIX: check the list order rules for Python FIX: refactor
		retval = None
		p = re.compile( r'[cC][rR][uU][dD]' ) # FIX: magic value
		for (i, v) in enumerate( self.get_REST_path() ):
			if p.match( v ):
				retval = i
				break
		return retval


	def get_from_path( self, offset ):
		retval = ''
		index = self.get_REST_CRUD_index()
		if index is not None:
			path = self.get_REST_path()
			if len( path ) > index + offset and path[index + offset].find( '.' ) == -1: # FIX: need a graceful solution
				retval = path[index + offset]
		return retval


	def get_format_from_path( self ):
		retval = ''
		path = self.get_REST_path()
		if len( path ) > 0:
			pieces = path[-1].split( '.' )
			if len( pieces ) > 0:
				retval = pieces[-1].lower()
		return retval


	def get_from_CGI( self, key ):
		return self.request.get( key )


	def get_model_from_path( self ):
		return self.get_from_path( 1 )


	def get_model_from_CGI( self ):
		return self.get_from_CGI( 'kind' ) # FIX: magic value


	def get_id_from_path( self ):
		return self.get_from_path( 2 )


	def get_id_from_CGI( self ):
		return self.get_from_CGI( 'id' ) # FIX: magic value


	def get_REST_model_T( self ):
		retval = None
		s = self.get_model_from_path()
		if not s:
			s = self.get_model_from_CGI()
		if s:
			retval = lightcrudmodel.make_kind_of_model_by_name( s, 'models' ) # FIX: magic value
		return retval


	def get_REST_model_id( self ):
		retval = self.get_id_from_path()
		if not retval:
			retval = self.get_id_from_CGI()
		return retval


	def create_REST_model_instance( self ):
		retval = None
		M = self.get_REST_model_T()
		if M is not None:
			retval = M()
		return retval


	def get_REST_model_instance( self ):
		retval = None
		M = self.get_REST_model_T()
		if M is not None:
			dbid = self.get_REST_model_id()
			if dbid:
				retval = M.get_by_id( int( dbid ) )
		return retval



class CrudCreateHandler( CrudHandler ):


	def post( self ):
		m = self.create_REST_model_instance()
		if m:
			lightcrudmodel.apply_dict( m, lightcrudmodel.from_format( self.request.body, self.get_format_from_path() ) )
			m.put()
			self.response.out.write( lightcrudmodel.to_format( lightcrudmodel.extract_dict( m ), self.get_format_from_path() ) )



class CrudReadHandler( CrudHandler ):


	def post( self ):
		M = self.get_REST_model_T()
		if M is not None:
			if self.get_REST_model_id():
				m = self.get_REST_model_instance()
				if m and m.is_saved():
					self.response.out.write( lightcrudmodel.to_format( lightcrudmodel.extract_dict( m ), self.get_format_from_path() ) )
			else:
				lm = [lightcrudmodel.extract_dict( m ) for m in M.all()]
				if lm:
					self.response.out.write( lightcrudmodel.to_format( lm, self.get_format_from_path() ) )
		else:
			llmm = []
			for modelname in models.bindings.keys():
				M = lightcrudmodel.make_kind_of_model_by_name( modelname, 'models' ) # FIX: magic value
				lm = [lightcrudmodel.extract_dict( m ) for m in M.all()]
				if lm:
					llmm.append( lm )
			if llmm:
				self.response.out.write( lightcrudmodel.to_format( llmm, self.get_format_from_path() ) )



class CrudUpdateHandler( CrudHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m and m.is_saved():
			lightcrudmodel.apply_dict( m, lightcrudmodel.from_format( self.request.body, self.get_format_from_path() ) )
			m.put()
			self.response.out.write( lightcrudmodel.to_format( lightcrudmodel.extract_dict( m ), self.get_format_from_path() ) )



class CrudDeleteHandler( CrudHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m:
			self.response.out.write( str( lightcrudmodel.extract_dict( m ) ) )
			self.response.out.write( lightcrudmodel.to_format( lightcrudmodel.extract_dict( m ), self.get_format_from_path() ) )
			m.delete()



def main():
	bindings = [
		('/Crud/.*', CrudCreateHandler),
		('/cRud/.*', CrudReadHandler),
		('/crUd/.*', CrudUpdateHandler),
		('/cruD/.*', CrudDeleteHandler),
		('/[cC][rR][uU][dD]/.*', CrudHandler),
		]
	app = webapp.WSGIApplication( bindings, debug=True )
	run_wsgi_app( app )



if __name__ == "__main__":
	main()


