import re
import requests
import os
import time
import base64

__all__ = ['Tomd', 'convert']

MARKDOWN = {
    'h1': ('\n# ', '\n'),
    'h2': ('\n## ', '\n'),
    'h3': ('\n### ', '\n'),
    'h4': ('\n#### ', '\n'),
    'h5': ('\n##### ', '\n'),
    'h6': ('\n###### ', '\n'),
    'code': ('`', '`'),
    'ul': ('', ''),
    'ol': ('', ''),
    'li': ('- ', ''),
    'blockquote': ('\n> ', '\n'),
    'em': ('**', '**'),
    'strong': ('**', '**'),
    'block_code': ('\n```\n', '\n```\n'),
    'span': ('', ''),
    'p': ('\n', '\n'),
    'p_with_out_class': ('\n', '\n'),
    'inline_p': ('', ''),
    'inline_p_with_out_class': ('', ''),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    'hr': ('\n---', '\n\n'),
    'thead': ('\n', '|------\n'),
    'tbody': ('\n', '\n'),
    'td': ('|', ''),
    'th': ('|', ''),
    'tr': ('', '\n')
}

BlOCK_ELEMENTS = {
    'h1': '<h1.*?>(.*?)</h1>',
    'h2': '<h2.*?>(.*?)</h2>',
    'h3': '<h3.*?>(.*?)</h3>',
    'h4': '<h4.*?>(.*?)</h4>',
    'h5': '<h5.*?>(.*?)</h5>',
    'h6': '<h6.*?>(.*?)</h6>',
    'hr': '<hr/>',
    'blockquote': '<blockquote.*?>(.*?)</blockquote>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'block_code': '<pre.*?><code.*?>(.*?)</code></pre>',
    'p': '<p\s.*?>(.*?)</p>',
    'p_with_out_class': '<p>(.*?)</p>',
    'thead': '<thead.*?>(.*?)</thead>',
    'tr': '<tr>(.*?)</tr>'
}

INLINE_ELEMENTS = {
    'td': '<td>(.*?)</td>',
    'tr': '<tr>(.*?)</tr>',
    'th': '<th>(.*?)</th>',
    'b': '<b>(.*?)</b>',
    'i': '<i>(.*?)</i>',
    'del': '<del>(.*?)</del>',
    'inline_p': '<p\s.*?>(.*?)</p>',
    'inline_p_with_out_class': '<p>(.*?)</p>',
    'code': '<code.*?>(.*?)</code>',
    'span': '<span.*?>(.*?)</span>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'li': '<li.*?>(.*?)</li>',
    'img': '<img.*?src=\"(.*?)\".*?>(.*?)(</)?',
    'a': '<a.*?href="(.*?)".*?>(.*?)</a>',
    'em': '<em.*?>(.*?)</em>',
    'strong': '<strong.*?>(.*?)</strong>'
}

DELETE_ELEMENTS = ['<span.*?>', '</span>', '<div.*?>', '</div>']


class Element:
    def __init__(self, start_pos, end_pos, content, tag,options, is_block=False):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.content = content.strip()
        self._elements = []
        self.is_block = is_block
        self.tag = tag
        self.options = options
        self._result = None

        if self.is_block:
            self.parse_inline()

    def __str__(self):
        wrapper = MARKDOWN.get(self.tag)
        self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])
        return self._result

    def parse_inline(self):
        for tag, pattern in INLINE_ELEMENTS.items():

            if tag == 'img':
                pattern = re.compile(pattern)
                match = pattern.search(self.content)
                if match:
                    url = match.group(1)
                    # print(self.content,url)
                    # 勒索后缀，勒索信文件名。 加密我分析了一部分。
                    # 
                    # | | | | 
                    localimg = self.options["localimg"] 
                    # 如果需要download img
                    if localimg and url and "store" in self.options and "img" in self.options:
                        base = self.options["base"]
                        store = self.options["store"]
                        img = self.options["img"]
                        article = self.options["article"]
                        if not os.path.exists(os.path.join( base,store,img,article )):
                            os.makedirs( os.path.join( base,store,img,article ) )
                        if url.startswith("http"):
                            print("[*] download image from url: {} .".format(url))
                            filename = url.split("/")[-1]
                            imagePath = os.path.join(base,store,img,article,filename)
                            try:
                                response = requests.get(url)
                                if response.status_code!=200:
                                    content = b"not found: {}" + url.encode()
                                else:
                                    content = response.content
                            except Exception as e:
                                content = b"not found: {}" + url.encode()
                            with open(imagePath,"wb") as fd:
                                fd.write(content)
                            self.content = self.content.replace(url, os.path.join("./",img,article,filename))
                        elif url.startswith("data:image"):
                            print("[*] download image from data base64 .")
                            filename = "{}.png".format(int(time.time()*1000))
                            imagePath = os.path.join(base,store,img,article,filename)
                            data = url.split(",")[-1].encode()
                            content = base64.b64decode(data)
                            with open(imagePath,"wb") as fd:
                                fd.write(content)
                        
                self.content = re.sub(pattern, '![\g<2>](\g<1>)\g<3>', self.content)
            elif tag == 'a':
                self.content = re.sub(pattern, '[\g<2>](\g<1>)', self.content)
            elif self.tag == 'ul' and tag == 'li':
                self.content = re.sub(pattern, '- \g<1>', self.content)
            elif self.tag == 'ol' and tag == 'li':
                self.content = re.sub(pattern, '1. \g<1>', self.content)
            elif self.tag == 'thead' and tag == 'tr':
                self.content = re.sub(pattern, '\g<1>\n', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'th':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'td':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            else:
                wrapper = MARKDOWN.get(tag)
                self.content = re.sub(pattern, '{}\g<1>{}'.format(wrapper[0], wrapper[1]), self.content)


class Tomd:
    def __init__(self, html='', options=None):
        self.html = html
        self.options = options
        self._markdown = ''

    def convert(self, html):
        elements = []
        for tag, pattern in BlOCK_ELEMENTS.items():
            for m in re.finditer(pattern, html, re.I | re.S | re.M):
                element = Element(start_pos=m.start(),
                                  end_pos=m.end(),
                                  content=''.join(m.groups()),
                                  tag=tag,
                                  options=self.options,
                                  is_block=True)
                can_append = True
                for e in elements:
                    if e.start_pos < m.start() and e.end_pos > m.end():
                        can_append = False
                    elif e.start_pos > m.start() and e.end_pos < m.end():
                        elements.remove(e)
                if can_append:
                    elements.append(element)

        elements.sort(key=lambda element: element.start_pos)
        self._markdown = ''.join([str(e) for e in elements])

        for index, element in enumerate(DELETE_ELEMENTS):
            self._markdown = re.sub(element, '', self._markdown)
        return self._markdown

    @property
    def markdown(self):
        self.convert(self.html)
        return self._markdown


_inst = Tomd()
convert = _inst.convert