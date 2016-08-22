#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "html")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("calculator.html")

    def post(self):
        number1 = self.request.get("number1")
        number2 = self.request.get("number2")
        operator = self.request.get("operator")
        if str(number1) == "" or str(number2) == "":
            result = "Prosimo, vpišite števili v označeni polji."
        else:
            if operator == "+":
                result = float(number1) + float(number2)
            elif operator == "-":
                result = float(number1) - float(number2)
            elif operator == "x" or operator == "X" or operator == "*":
                result = float(number1) * float(number2)
            elif operator == "/" or operator == ":":
                result = float(number1) / float(number2)
            else:
                result = "Prosimo, vpišite pravilen matematični operator."
        self.write(result)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler)
], debug=True)
