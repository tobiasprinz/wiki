from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from datetime import datetime
import secrets
import markdown
import peewee


DB = peewee.SqliteDatabase('wiki.db')


class Page(peewee.Model):
    pagename = peewee.CharField(unique=True)
    content = peewee.CharField()
    last_modified = peewee.DateTimeField()

    class Meta:
        database = DB


class PageController():
	def __init__(self):
		self.db = DB
		self.db.connect()
		self.db.create_tables([Page])


	def look_for_page(self, pagename):
		try:
			return Page.get(Page.pagename == pagename)
		except Page.DoesNotExist:
			return None
		

	def store_page(self, page):
		page.last_modified = datetime.now()
		page.save()

	def all_pages(self):
		return Page.select()


class PageView():
	def __init__(self, template=None):
		self.template = '''
			<!DOCTYPE html>
			<html lang="en">
			  <head>
			    <meta charset="utf-8">
			    <title>{title}</title>
			    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
			  </head>
			  <body>
			  	<nav><a href="/">Home</a></nav>
			  	<main class="container">
			    	{body}
			    </main>
			  </body>
			</html>
		'''


	def render(self, title=None, content=None):
		return self.template.format(title=title, body=content)


	def view(self, page):
		return self.render(page.pagename, markdown.markdown(page.content, extensions=['toc']))


	def edit(self, page):
		content = '''
			<form action="/{pagename}/save" method="post">
				<textarea name="content">{content}</textarea>
				<input type="submit" value="submit">Submit</input>
			</form>
			'''.format(pagename=page.pagename, content=page.content)
		return self.render(page.pagename, content)


	def list(self, pages):
		retval = '<ul>'
		for page in pages:
			retval += '<li><a href="{pagename}">{pagename}</a></li>'.format(pagename=page.pagename)
		return self.render('List', retval + '</ul>')


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
pc = PageController()


@app.route('/', methods=['get'])
def serve_list():
	p = pc.all_pages()
	return PageView().list(p)


@app.route('/<pagename>', methods=['get'])
def serve_page(pagename):
	p = pc.look_for_page(pagename)
	if p:
		return PageView().view(p)
	else:
		return redirect(url_for('serve_edit_view', pagename=pagename))


@app.route('/<pagename>/edit', methods=['get', 'post'])
def serve_edit_view(pagename):
	p = pc.look_for_page(pagename)
	if not p:
		p = Page(pagename=pagename, content='')
	return PageView().edit(p)


@app.route('/<pagename>/save', methods=['post'])
def serve_save_view(pagename):
	p = pc.look_for_page(pagename)

	if p:
		p.content = request.form['content']
	else:
		p = Page(pagename=pagename, content=request.form['content'])

	pc.store_page(p)
	flash("Page {} was stored.".format(pagename))
	return redirect(url_for('serve_page', pagename=pagename))