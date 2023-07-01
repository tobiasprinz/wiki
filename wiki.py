from flask import Flask
from flask import request
from views import PageView
from controllers import PageController
from models import Page


app = Flask(__name__)

pc = PageController()


@app.route('/', methods=['get'])
def serve_list():
	p = pc.all_pages()
	return PageView().list(p)


@app.route('/<pagename>', methods=['get'])
def serve_page(pagename):
	p = pc.look_for_page(pagename)
	return PageView().view(p)


@app.route('/<pagename>/edit', methods=['get'])
def serve_edit_view(pagename):
	p = pc.look_for_page(pagename)
	return PageView().edit(p)


@app.route('/<pagename>/save', methods=['post'])
def serve_save_view(pagename):
	p = Page(pagename=request.form['pagename'], content=request.form['content'])
	pc.store_page(p)
	return PageView().view(p)