#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Bernardo Heynemann <heynemann@gmail.com>
# Copyright (C) 2009 Gabriel Falcão <gabriel@nacaolivre.org>
#
# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.opensource.org/licenses/osl-3.0.php
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

NAME_DICT = {}
URL_DICT = {}

class MetaPage(type):
    def __init__(cls, name, bases, attrs):
        if name not in ('MetaPage', 'Page'):

            if not attrs.has_key('url'):
                raise NotImplementedError('%r does not contain the attribute url' % cls)

            url = attrs['url']
            if not isinstance(url, basestring):
                raise TypeError('%s.url must be a string or unicode. Got %r(%r)' % (name, url.__class__, url))

            NAME_DICT[name] = cls
            if URL_DICT.has_key(url):
                URL_DICT[url].append(cls)
            else:
                URL_DICT[url] = [cls]


        super(MetaPage, cls).__init__(name, bases, attrs)

class PageRegistry(object):
    @classmethod
    def get_by_name(cls, name):
        name = name.replace(" ", "")
        return NAME_DICT.get(name)

    @classmethod
    def all_by_url(cls, url):
        return URL_DICT.get(url)

class Page(object):
    __metaclass__ = MetaPage
    '''Class that defines a page model.'''

    Button = "button"
    Checkbox = "checkbox"
    Div = "div"
    Image = "image"
    Link = "link"
    Page = "page"
    RadioButton = "radio_button"
    Select = "select"
    Textbox = "textbox"
    Element = '*'

    def __init__(self):
        '''Initializes the page with the given url.'''
        self.registered_elements = {}
        if hasattr(self, "register"):
            self.register()

    def get_registered_element(self, element_key):
        if not self.registered_elements.has_key(element_key):
            return None
        return self.registered_elements[element_key]

    def register_element(self, element_key, element_locator):
        self.registered_elements[element_key] = element_locator

