import sys
import glob
import wiki
import os


def import_markdown_files(path):
	for file in glob.glob(path):
		with open(file, encoding='utf-8') as f:
			pagename = os.path.splitext(os.path.basename(file))[0]
			content = ''.join(f.readlines())
		p = wiki.pc.look_for_page(pagename)
		if not p:
			print('Creating new page: {}'.format(pagename))
			p = wiki.Page(pagename=pagename, content=content)
		else:
			print('Overwriting existing page: {}'.format(pagename))
			p.content = content
		wiki.pc.store_page(p)
		


def export_markdown_files(path):
	pass


if __name__ == "__main__":
	if len(sys.argv) == 3 and sys.argv[1] == 'import':
		import_markdown_files(sys.argv[2])
	elif len(sys.argv) == 3 and sys.argv[1] == 'export':
		export_markdown_files(sys.argv[2])
	else:
		print("Usage:\npython {} [import|export] path".format(sys.argv[0]))
