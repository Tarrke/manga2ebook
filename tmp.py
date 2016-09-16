#!/usr/bin/python

from ebooklib import epub

book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample Ebook')
book.set_language('en')

book.add_author('Tarrke')

book.set_cover("image.jpg", open('cover.jpg', 'rb').read())


# create page 1
c1 = epub.EpubHtml(title='Page #1', file_name='page_1.xhtml', lang='en')
c1.content=u'<div><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="0 0 590 750" preserveAspectRatio="none"><image width="590" height="750" xlink:href="1_0.png"/></svg></div>'

c2 = epub.EpubHtml(title='Page #2', file_name='page_2.xhtml', lang='en')
c2.content=u'<div><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="0 0 590 750" preserveAspectRatio="none"><image width="590" height="750" xlink:href="2_0.png"/></svg></div>'

book.add_item(c1)
book.add_item(c2)

im1 = open('1_0.png', 'rb').read()
im2 = open('2_0.png', 'rb').read()

img1 = epub.EpubItem(uid="1_0.png", file_name="1_0.png", media_type="image/png", content=im1)
img2 = epub.EpubItem(uid="2_0.png", file_name="2_0.png", media_type="image/png", content=im2)


book.add_item(img1)
book.add_item(img2)

#book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'), 
#			(epub.Section('Simple book'), 
#			(c1, c2))
#			)

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

book.spine = ['cover', c1, c2]

epub.write_epub('test.epub', book, {})
