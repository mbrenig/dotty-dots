import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from models import *

from util import simplejson
from util.cgi import unescape

class EditorPage(webapp.RequestHandler):
	def get(self):
	
		chr_to_edit = self.request.get("chr")
		if len(chr_to_edit) != 1:
			raise Exception("Bad length of character: '%s'." % chr_to_edit)
			
		template_values = {'chr_to_edit': chr_to_edit}
			
		char_json = CharJson.all().filter('chr =', chr_to_edit).get()

		if char_json:
			try:
				json = simplejson.loads(char_json.json)
				points = json['points']
				width = json['width']
				template_values['points_list'] = points
				template_values['chr_width'] = width
			except:
				pass

		path = os.path.join(os.path.dirname(__file__), 'secret-character-editor', 'editor_template.html')
		self.response.out.write(template.render(path, template_values))


class SaveCharData(webapp.RequestHandler):
	def post(self):
		json = self.request.get("data")
		logging.error("json = %s" % json)
		
		chr_to_edit = self.request.get("chr_to_edit")
		logging.error("chr_to_edit = %s" % chr_to_edit)
				
		char_json = CharJson.all().filter('chr = ', chr_to_edit).get()
		
		if char_json:
			char_json.json = json
			char_json.put()
		else:
			char_json = CharJson(chr=chr_to_edit,json=json)
			char_json.put()
			
		return "Thanks!"
		
class BuildJsonBlock(webapp.RequestHandler):
	def get(self):
		char_json_list = CharJson.all().fetch(100)
		alphabet = {}
		for char_json in char_json_list:
			alphabet[char_json.chr] = simplejson.loads(char_json.json)
			
		js_string = "document.alphabet={"
		letters = []
		for (character, char_defn) in alphabet.iteritems():
			
			letter_string = None
			if len(character) == 1:
				letter_string = "A%x:{" % ord(character)
			elif character[0] == '&' and character[-1] == ';':
				# Unescape the character.
				special_char = unescape(character)
				if len(special_char) == 1:
					letter_string = "A%x:{" % ord(special_char)
					
			if letter_string is None:
				logging.error("Character in datastore '%s' could not be cast to hex" % character)
				continue
				
			letter_string += "W:%s,P:[" % char_defn["width"]
			
			point_list = []
			for point_dict in char_defn["points"]:
				point_string = "[%s,%s,%s,%s]" % (point_dict["x"],
												  point_dict["y"],
												  point_dict["s"],
												  point_dict["f"])
				point_list.append(point_string)
			full_point_string = ",".join(point_list)
			
			letter_string += full_point_string
			letter_string += "]}"
			letters.append(letter_string)
		
		js_string += ",".join(letters)
		js_string += "};"
		
		self.response.headers["Content-Type"] = "text"
		self.response.out.write( js_string )
		

application = webapp.WSGIApplication(
									 [('/secret-character-editor/edit.*', EditorPage),
									  ('/secret-character-editor/save.*', SaveCharData),
									  ('/secret-character-editor/alphabet.js', BuildJsonBlock)],
									 debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()