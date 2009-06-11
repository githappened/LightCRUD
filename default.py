


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
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app



class HomePage( webapp.RequestHandler ):


	def get( self ):
		self.response.out.write( template.render( 'template/default.xml', {'title': 'lightsvg', 'titleleaf': 'home'} ) ) # FIX: relative path?



def main():
	bindings = [
		('/.*', HomePage),
		]
	app = webapp.WSGIApplication( bindings, debug=True )
	run_wsgi_app( app )



if __name__ == "__main__":
	main()


