###############################################################
# The controller for the records from Heroku Database to be exchanged
# to the templates. The data is filtered here and called by
# the html to execute a render of a specific html page. The
# data is being sent over the Flask framework due to ease
# of use and the ability to handle large amounts of lists
#
# Edited: Logan
# Edited: Grant
##############################################################


from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#from bookshelf import oauth2
from flask import Blueprint, current_app, redirect, render_template, request, \
    	session, url_for, Flask, send_file, Markup
from operator import itemgetter
import httplib2
from extra import psql3, unknownPieChart, proposerPieChart, proposerChart, get_values, get_values_adv, get_final, get_valuesx, get_valuesy, gcount_authors, gcount_contributors, gwhole_list, psql2, psql, count_authors
import os
import csv
import random
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objs as go
from datetime import datetime
from pytz import timezone
import time

try:
   	import argparse
   	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
   	flags = None

#count of solvers
count = 0
#count of contributors
count2 = 0

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"

##############################################################
# Search method to find an author an a specific index on 
# specific page number
# Groups by 50 authors max
##############################################################
@app.route("/author/<page>/<author>")
def search2(page, author):
    	temp = int(page)
    	list = get_valuesy(50,temp,author)
    	count = gcount_authors()
    	count2 = gcount_contributors()
    	return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2, search=temp, bit=1,svalue=author)

##############################################################
# Links to advnaced search form to eneter attributes
# Not currently being used
##############################################################   
@app.route("/advanced")
def advanced():
    	return render_template("form.html")
		
##############################################################
# Links to advnaced search form to eneter attributes
# Not currently being used
##############################################################   
@app.route("/statistics")
def stats():
	place = proposerChart()
	pie = proposerPieChart()
	pieknown = unknownPieChart()
    	return render_template("statistics.html", div_placeholder=Markup(place), pies=Markup(pie), known=Markup(pieknown))

##############################################################
# Search method that looks for a value in the proposer that 
# links with user input in search field
# Groups by 50 authors max
##############################################################
@app.route("/tabs/<page>/<search>")
def search(page, search):
    	temp = int(page)
    	list = get_valuesx(50,temp,search)
    	count = gcount_authors()
    	count2 = gcount_contributors()
    	return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2, search=temp,bit=2,svalue=search)
	
##############################################################
# Search method that looks for a value in the proposer that 
# links with user input in search field
# Groups by 50 authors max
##############################################################
@app.route("/tabs/<page>/<number>/<etvol>/<etvol2>/<etdate>/<etdate2>/<proposer>/<solver>/<solvol>/<solvol2>/<soldate>/<soldate2>/<mqvol>/<mqvol2>/<qtype>/<un>")
def advanded_search(page, number, etvol, etvol2, etdate, etdate2, proposer, solver, solvol, solvol2, soldate, soldate2, mqvol, mqvol2, qtype, un):
    	temp = int(page)
    	cur = psql2(number, etvol, etvol2, proposer, solver, qtype, un)
    	list = get_values_adv(50,temp,cur, mqvol, mqvol2, solvol, solvol2, etdate, etdate2, soldate, soldate2)
    	count = gcount_authors()
    	count2 = gcount_contributors()
    	search = number + "/" +etvol+ "/" +etvol2+ "/" +etdate+ "/" +etdate2+ "/" +proposer+ "/" +solver+ "/" +solvol+ "/" +solvol2+"/" +soldate+"/" +soldate2+ "/" +mqvol+ "/" +mqvol2+ "/" +qtype+ "/"+un
	return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2, search=temp,bit=3,svalue=search)

##############################################################
# Allows users to go through an sorted table by questin number
# only 
# Groups by 50 authors max
##############################################################
@app.route("/tabs/<page>")
def tabsNext(page):
    	temp = int(page)
    	cur = psql()
    	list = get_values(50, temp, cur)
    	count = gcount_authors()
    	count2 = gcount_contributors()
    	return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2, search=temp,bit=0,svalue='')

##############################################################
# Pulls the data from api at the beginning of each interaction
# with web application
# Groups by 50 authors max
##############################################################
@app.route("/tabs", methods=['GET', 'POST'])
def tabs():
	cur = psql()
    	if(request.method == 'GET'):
       		list = get_values(50, '', cur); 
       		count = gcount_authors()
       		count2 = gcount_contributors()
       		return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2)
    	else:
       		list = get_values(0, '', cur);  
       		count = gcount_authors()
       		count2 = gcount_contributors()
       		return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2)

##############################################################
# Pulls the data from api at the beginning of each interaction
# with web application
# Groups by 50 authors max
##############################################################
@app.route("/")
def hello():
	cur = psql()
	list = get_values(50, '', cur) 
	count = gcount_authors()
	count2 = gcount_contributors()	
	return render_template("bookshelf_templates_tabs.html", lists=list, authors=count, solvers=count2)


##############################################################
# This downloads a csv file of the data that was queried
##############################################################
@app.route("/downloadablesw")
def downloadable():
	list = get_final()
	
	with open('expa.csv','w') as myfile:
        	wr = csv.writer(myfile)
        	wr.writerow(['NUM','PROPOSER','ET VOL','DATE','SOLVERS','ET VOL','DATE','MQ VOL','TYPE'])
        	for item in list:
            		wr.writerow([item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]])
		myfile.close()
	now=datetime.now(timezone('US/Eastern'))
	st=now.strftime('%Y-%m-%d.%I-%M%p')
	value="ETquery"+st+".csv"
	return send_file("expa.csv", mimetype="csv", attachment_filename=value, as_attachment=True, cache_timeout=0)
	
		 

if __name__ == "__main__":
    	port = int(os.environ.get("PORT", 8080))
    	app.run(host='0.0.0.0', port=port)
