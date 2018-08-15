from __future__ import print_function
import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request

from report import *

import pandas as pd

from collections import defaultdict
import re

from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

import sqlite3

project_dir = os.path.dirname(os.path.abspath(__file__))
database_local_addr = '44_logfile.db'
database_file = 'sqlite:///' + os.path.join(os.path.dirname(os.path.realpath(__file__)), database_local_addr)
table_name = 'Pampers_Pure_utf8'
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACKS_MODIFICATIONS"] = False

cnx = sqlite3.connect(database_local_addr)
log = pd.read_sql_query("SELECT * FROM " + table_name, cnx)


db = SQLAlchemy(app)

class open(db.Model):
    __tablename__ = table_name
    Product = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Category = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Brand = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    RespondentId = db.Column(db.String(400), unique=False, nullable=False, primary_key=True)
    #External_RespondentId = db.Column('External RespondentId',db.String(400), unique=False, nullable=False, primary_key=False)
    Platform = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Experiment = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Prod_id = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Action = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Bought = db.Column('Bought',db.Integer, unique=False, nullable=True, primary_key=False)
    Timestamp = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_id = db.Column('Detail id',db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_url = db.Column('Detail url',db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_type = db.Column('Detail type',db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_price = db.Column('Detail price',db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_name = db.Column('Detail name',db.String(400), unique=False, nullable=False, primary_key=False)
    Detail_position = db.Column('Detail position',db.String(400), unique=False, nullable=False, primary_key=False)
    img_pos = db.Column('img_pos',db.Float, unique=False, nullable=False, primary_key=False)
    timespent = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
    #size = db.Column(db.String(400), unique=False, nullable=False, primary_key=False)



#def query_to_list(rset):
#    result = []
#    for obj in rset:
#        instance = inspect(obj)
#        items = instance.attrs.items()
#        result.append([x.value for _,x in items])
#    return instance.attrs.keys(), result

def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result

def regex_to_txt(string):
    if string=='.*':
        string='[All]'
    string=string.replace('.*', '[Anything]')
    return string

def txt_to_regex(string):
    if string=='[All]':
        string='.*'
    string=string.replace('[Anything]','.*')
    return string

def list_to_regex(list,sep):
    string=list.split(sep)
    return txt_to_regex(string)

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).replace("\n", ' | ').replace("                                        ", ' | ').replace("\t", ' | ')

@app.route('/', methods=["GET", "POST"])
def home():
    answers=None
    word=None
    df=None
    '''if request.form:
        try:
            word = request.form.get("word")
            answers = open.query.filter(open.Product.like('%'+word+'%'))
        except Exception as e:
            print("Failed to search answer")
            print(e)
    elif request.args:
        try:
            word = request.args.get("word")
            answers = open.query.filter(open.Product.like('%'+word+'%'))
        except Exception as e:
            print("Failed to search answer")
            print(e)
    else :
        answers = open.query.all()'''
    col_products='Product'
    col_category='Category'
    val_category='.*'
    category_list=['.*']

    contains_product=True
    products=''
    product_list=['.*']

    col='Platform'
    value_list=['.*']

    col_2='Experiment'
    value_2_list=['.*']

    tables=[]
    csv_tables=[]

    if request.form:
        try:
            products = request.form.get("products")
            if products != '':
                product_list=list_to_regex(products)

            categories = request.form.get("categories")
            if categories != '':
                category_list = list_to_regex(categories)

            values = request.form.get("values")
            if values != '':
                value_list = list_to_regex(values)

            values_2 = request.form.get("values_2")
            if values_2 != '':
                value_2_list = list_to_regex(values_2)

        except Exception as e:
            print("Failed to search answer")
            print(e)

    elif request.args:
        try:
            products = request.args.get("products")
            if products != '':
                product_list=products.split(',')

            categories = request.args.get("categories")
            if categories != '':
                category_list = categories.split(',')

            values = request.args.get("values")
            if values != '':
                value_list = platforms.split(',')

            values_2 = request.args.get("values_2")
            if values_2 != '':
                value_2_list = platforms.split(',')

        except Exception as e:
            print("Failed to search answer")
            print(e)
    else :
        answers = open.query.all()


    columns_tbl=[{'type':'action','name':['pageview']},
            {'type':'action','name':['pageview','bought']},
            {'type':'action','name':['descr_technical_in','descr_specs_in','descr_short_in','descr_long_in']},
            {'type':'action','name':['descr_technical_in']},
            {'type':'action','name':['descr_specs_in']},
            {'type':'action','name':['descr_short_in']},
            {'type':'action','name':['descr_long_in']},
            {'type':'action','name':['emerch_content_in','emerch_content2_in','emerch_content3_in','emerch_content4_in','aplus_content_in']},
            {'type':'action','name':['aplus_content_in']},
            {'type':'action','name':['emerch_content_in']},
            {'type':'action','name':['emerch_content2_in']},
            {'type':'action','name':['emerch_content3_in']},
            {'type':'action','name':['emerch_content4_in']},
            {'type':'action','name':['review_in']}]

    for product in product_list:
        for category in category_list:
            for value in value_list:
                for value_2 in value_2_list:
                    filters=[
                            {'column':col,'content':value},
                            {'column':col_2,'content':value_2},
                            {'column':col_category,'content':category},
                            {'column':col_products,'content':product}
                            ]
                    #import pdb;pdb.set_trace()
                    #prnt(description_report(log,columns_tbl,filters,sigtest=False,fraction_digits=2,ecommerce_metrics=False,contains_product=contains_product).to_html())
                    title="<h3>Product : "+regex_to_txt(product)+"""<br/>
                                        Categories : """+regex_to_txt(category)+"""</h3>
                                        <h4>"""+col+""": """+regex_to_txt(value)+""" -
                                        """+col_2+""" : """+regex_to_txt(value_2)+"""
                                        </h4>"""
                    csv_table=description_report(log,columns_tbl,filters,sigtest=False,fraction_digits=2,ecommerce_metrics=False,contains_product=contains_product)
                    cols = csv_table.columns.tolist()
                    csv_table=csv_table[cols[1:]]
                    tables.append(HTML(title+csv_table.to_html()))
                    csv_table_columns=csv_table.columns

                    #import pdb; pdb.set_trace()
                    csv_table['Filters']=remove_html_tags(title)
                    cols = csv_table.columns.tolist()
                    csv_table=csv_table[cols[-1:]+cols[:-1]]
                    #csv_table=csv_table[['Filters']+csv_table_columns]

                    csv_tables.append(csv_table)


    #import pdb; pdb.set_trace()
    pd.concat(csv_tables).to_csv('filename.csv')

    return render_template("index.html", answers=answers, products=products,tables=tables)

if __name__ == '__main__':
    # Engine & session
    #engine = create_engine('sqlite:///:memory:', echo=True)
    #open.metadata.create_all(engine)
    # Query
    #rset = open.query.all()
    # Give me a DataFrame
    # Inconvenient: it's not well ordered (e.g. 'id' is not the first)
    #df = pd.DataFrame(query_to_dict(rset))
    ##print(df.head(3))
    #names, data = query_to_list(rset)
    #df2 = pd.DataFrame.from_records(data, columns=names)
    app.run(host='0.0.0.0',debug=True)
