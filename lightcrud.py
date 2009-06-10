


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



# FIX: refactor the following tedium



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
		p = re.compile( r'[cC][rR][uU][dD]' )
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
			if len( path ) > index + offset:
				retval = path[index + offset]
		return retval


	def get_from_CGI( self, key ):
		return self.request.get( key )


	def get_model_from_path( self ):
		return self.get_from_path( 1 )


	def get_model_from_CGI( self ):
		return self.get_from_CGI( 'kind' )


	def get_id_from_path( self ):
		return self.get_from_path( 2 )


	def get_id_from_CGI( self ):
		return self.get_from_CGI( 'id' )


	def get_REST_model_T( self ):
		retval = None
		s = self.get_model_from_path()
		if not s:
			s = self.get_model_from_CGI()
		if s:
			retval = models.make_kind_of_model_by_name( s )
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
			m.apply_dict( self.get_REST_dict() )
			m.put()
			self.response.out.write( str( m.extract_dict() ) )



class JSONCrudCreateHandler( CrudCreateHandler ):


	def post( self ):
		m = self.create_REST_model_instance()
		if m:
			m.apply_dict( self.get_REST_dict() )
			m.put()
			self.response.out.write( m.toJSON() )



class CrudReadHandler( CrudHandler ):


	def post( self ):
		M = self.get_REST_model_T()
		if M is not None:
			if self.get_REST_model_id():
				m = self.get_REST_model_instance()
				if m and m.is_saved():
					self.response.out.write( str( m.extract_dict() ) )
			else:
				lm = [m.extract_dict() for m in M.all()]
				if lm:
					self.response.out.write( str( lm ) )
		else:
			llmm = []
			for modelname in models.bindings.keys():
				M = models.make_kind_of_model_by_name( modelname )
				lm = [m.extract_dict() for m in M.all()]
				if lm:
					llmm.append( lm )
			if llmm:
				self.response.out.write( str( llmm ) )



class JSONCrudReadHandler( CrudReadHandler ):


	def post( self ):
		M = self.get_REST_model_T()
		if M is not None:
			if self.get_REST_model_id():
				m = self.get_REST_model_instance()
				if m and m.is_saved():
					self.response.out.write( m.toJSON() )
			else:
				lm = [m.extract_dict() for m in M.all()]
				if lm:
					self.response.out.write( lightcrudmodel.toJSON( lm ) )
		else:
			llmm = []
			for modelname in models.bindings.keys():
				M = models.make_kind_of_model_by_name( modelname )
				lm = [m.extract_dict() for m in M.all()]
				if lm:
					llmm.append( lm )
			if llmm:
				self.response.out.write( lightcrudmodel.toJSON( llmm ) )



class CrudUpdateHandler( CrudHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m and m.is_saved():
			m.apply_dict( self.get_REST_dict() )
			m.put()
			self.response.out.write( str( m.extract_dict() ) )



class JSONCrudUpdateHandler( CrudUpdateHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m and m.is_saved():
			m.apply_dict( self.get_REST_dict() )
			m.put()
			self.response.out.write( m.toJSON() )



class CrudDeleteHandler( CrudHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m:
			self.response.out.write( str( m.extract_dict() ) )
			m.delete()



class JSONCrudDeleteHandler( CrudDeleteHandler ):


	def post( self ):
		m = self.get_REST_model_instance()
		if m:
			self.response.out.write( m.toJSON() )
			m.delete()



def main():
	bindings = [
		('/JSON/Crud/.*', JSONCrudCreateHandler),
		('/JSON/cRud/.*', JSONCrudReadHandler),
		('/JSON/crUd/.*', JSONCrudUpdateHandler),
		('/JSON/cruD/.*', JSONCrudDeleteHandler),
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


