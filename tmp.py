from ebooklib import epub

book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample Ebook')
book.set_language('en')

book.add_author('Tarrke')

book.set_cover("image.jpg", open('cover.jpg', 'rb').read())

# create chapter
c1 = epub.EpubHtml(title='Intro-spection', file_name='chap_01.xhmtl', lang='en')
c1.content=u'<h1>Introduction</h1><p>Salut le monde.</p>'

c2 = epub.EpubHtml(title='About this book', file_name='about.xhtml', lang='en')
c2.content='<h1>About this book</h1><p>Helou, this is my book! There are many books, but this one is mine.</p>'

book.add_item(c1)
book.add_item(c2)

book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'), 
			(epub.Section('Simple book'), 
			(c1, c2))
			)

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style= '''
@namespace epub "http://www.idpf.org/2007/ops";
body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}
h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;     
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
'''

nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/cass", content=style)
book.add_item(nav_css)

book.spine = ['cover', 'nav', c1, c2]

epub.write_epub('test.epub', book, {})
