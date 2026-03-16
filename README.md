# flask-admin multiple sessions issue

Just a short app to reproduce multiple sessions with sqlalhemy

flask-admin issue for more context: [2831](https://github.com/pallets-eco/flask-admin/issues/2831)

## It is not a project, nor a fork

It is used only to prepare reproducable environment.

## Steps to reproduce
- clone it and run with `uv run main.py`
- try to create and "Art" and it will throw error that Team already exist in different session
- uncomment either `form_extra_fields` or `form_args` in ArtsView and it works fine
- Try to edit Art (add extra team, not name), Unique validator fails
- Change from `USE_CUSTOM_EQUATION = False` to `USE_CUSTOM_EQUATION = True`, editing works
- if `MODE = "anythong except lite"` it will run full sqlalchemy and creating/editing works without changing anything