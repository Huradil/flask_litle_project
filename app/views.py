from flask import render_template,request,redirect,url_for,flash

from . import app,db
from .models import Category,Item,User
from .forms import  CategoryForm,ItemForm,UserForm
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError


def index():
    items=Item.query.all()
    return render_template('item_list.html',items=items)


def category_create():
    form=CategoryForm()
    if request.method=='POST':
        if form.validate_on_submit():
            category=Category()
            form.populate_obj(category)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('categories'))
        else:
            print(form.errors)
    return render_template('standart_form.html',form=form)


def category_list():
    categories=Category.query.all()
    return render_template('category_list.html',categories=categories)

def category_update(id):
    category=Category.query.get(id)
    form=CategoryForm(obj=category)
    if request.method=='POST':
        form.populate_obj(category)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    else:
        print(form.errors)
    return render_template('standart_form.html',form=form)


@login_required
def item_create():
    form = ItemForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            item = Item()
            form.populate_obj(item)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standart_form.html', form=form)


@login_required
def item_update(id):
    item=Item.query.get(id)
    form = ItemForm(obj=item)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(item)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standart_form.html', form=form)


@login_required
def item_delete(id):
    item=Item.query.get(id)
    if request.method=='POST':
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html',item=item)

def register():
    title='регистрация'
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
            user=User()
            form.populate_obj(user)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                flash('такой пользователь уже существует','danger')
                return render_template('register.html', form=form, title=title)
            else:
                flash('Вы успешно зарегистрировались',"succes")
                return redirect(url_for('login'))
        else:
            print(form.errors)
    return render_template('register.html',form=form,title=title)


def login():
    title='авторизация'
    form=UserForm()
    if request.method=='POST':
        if form.validate_on_submit():
            user=User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                print('Неправильные данные')
        else:
            print(form.errors)
    return render_template('register.html',form=form,title=title)


def logout():
    logout_user()
    return redirect(url_for('login'))



