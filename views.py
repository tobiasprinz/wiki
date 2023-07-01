import markdown


class PageView():
	def __init__(self, template=None):
		self.template = template

	def view(self, page):
		return markdown.markdown(page.content)

	def edit(self, page):
		return '''
			<form action="/{pagename}/save" method="post">
				<input type="hidden" name="pagename" value="{pagename}" />
				<textarea name="content">{content}</textarea>
				<input type="submit" value="submit">Submit</input>
			</form>
			'''.format(pagename=page.pagename, content=page.content)

	def list(self, pages):
		retval = '<ul>'
		for page in pages:
			retval += '<li><a href="{pagename}">{pagename}</a></li>'.format(pagename=page.pagename)
		return retval + '</ul>'