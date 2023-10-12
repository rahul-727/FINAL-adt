from flask import*
from database import *
import uuid

staff=Blueprint('staff',__name__)

@staff.route("/staffhome")
def staffhome():
	return render_template("staffhome.html")

@staff.route("/manage_timeslot",methods=['post','get'])
def manage_timeslot():
	data={}
	q="select * from timeslot"
	res=select(q)
	data['view']=res
	if "submit" in request.form:
		date=request.form['date']
		time=request.form['time']
		q="insert into timeslot values(null,'%s','%s')"%(date,time)
		insert(q)
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=="update":
		q="select * from timeslot where Timeslot_id='%s'"%(cid)
		res=select(q)
		data['time']=res 

	if "update" in request.form:
		date=request.form['date']
		time=request.form['time']
		q="update timeslot set Date='%s',Time='%s' where Timeslot_id='%s'"%(date,time,cid)
		update(q)
		return redirect(url_for("staff.manage_timeslot"))
	return render_template("staff_manage_timeslot.html",data=data)


@staff.route("/manage_tables",methods=['post','get'])
def manage_tables():
	data={}
	q="select * from tables INNER JOIN category USING(Category_id)"
	res=select(q)
	data['view']=res
 
	q="select * from category"
	res=select(q)
	data['category']=res
 
	if "submit" in request.form:
		tnum=request.form['tnum']
		cat=request.form['cat']
		q="INSERT INTO tables VALUES(NULL,'%s','%s','pending')"%(tnum,cat)
		insert(q)
		return redirect(url_for("staff.manage_table"))
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=="update":
		q="select * from tables where Table_id='%s'"%(cid)
		res=select(q)
		data['time']=res 

	if "update" in request.form:
		tnum=request.form['tnum']
		cat=request.form['cat']
		q="update tables set Table_num='%s',Category_id='%s' where Table_id='%s'"%(tnum,cat,cid)
		update(q)
		return redirect(url_for("staff.manage_tables"))
	return render_template("staff_manage_table.html",data=data)


@staff.route("/manage_category",methods=['post','get'])
def manage_category():
	data={}
	q="select * from category"
	res=select(q)
	data['view']=res
	if "submit" in request.form:
		cat=request.form['cat']
		price=request.form['price']

		
		q="INSERT INTO category VALUES(NULL,'%s','%s','1')"%(cat,price)
		insert(q)
		return redirect(url_for("admin.manage_category"))
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=="update":
		q="select * from category where Category_id='%s'"%(cid)
		res=select(q)
		data['time']=res 

	if "update" in request.form:
		cat=request.form['cat']
		price=request.form['price']
		q="update category set Category='%s',Category_price='%s' where Category_id='%s'"%(cat,price,cid)
		update(q)
		return redirect(url_for("staff.manage_category"))
	return render_template("staff_manage_category.html",data=data)


@staff.route("/manage_menu",methods=['post','get'])
def manage_menu():
	data={}
	q="select * from category"
	res=select(q)
	data['view']=res
	if "submit" in request.form:
		cat=request.form['category']
		menu=request.form['menu']
		img=request.files['img']
		path='static/images/'+str(uuid.uuid4())+img.filename
		img.save(path)
		q="insert into menu values(null,'%s','%s','%s','1')"%(cat,menu,rate,path)
		insert(q)

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None
	if action=="active":
		q="update menu set Status='1' where Menu_id='%s'"%(cid)
		update(q)
	if action=="inactive":
		q="update menu set Status='0' where Menu_id='%s'"%(cid)
		update(q)

	if action=="update":
		q="select * from category where Menu_id='%s'"%(cid)
		res=select(q)
		data['time']=res 

	if "update" in request.form:
		menu=request.form['menu']
		rate=request.form['rate']
		
		q="update menu set Menu='%s',Rate='%s' where Menu_id='%s'"%(cat,cid)
		update(q)
		return redirect(url_for("staff.manage_category"))
	return render_template("staff_manage_menu.html",data=data)

@staff.route("/view_booking",methods=['post','get'])
def view_booking():
	data={}
	q="select * from booking inner join customer using(Customer_id) inner join timeslot using(Timeslot_id) inner join tables using(Table_id)"
	res=select(q)
	data['view']=res
	return render_template("staff_view_booking.html",data=data)
@staff.route("/manage_extraservice",methods=['post','get'])
def manage_extraservice():
	data={}
	q="select * from extraservice"
	res=select(q)
	data['view']=res
	if "submit" in request.form:
		extra=request.form['extra']
		des=request.form['des']

		
		q="INSERT INTO extraservice VALUES(NULL,'%s','%s')"%(extra,des)
		insert(q)
		return redirect(url_for("staff.manage_extraservice"))
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None

	if action=="update":
		q="select * from extraservice where Extraservice_id='%s'"%(cid)
		res=select(q)
		data['time']=res 

	if "update" in request.form:
		extra=request.form['extra']
		des=request.form['des']
		
		q="update extraservice set Extraservice_name='%s',description='%s' where Extraservice_id='%s'"%(extra,des,cid)
		update(q)
		return redirect(url_for("staff.manage_extraservice"))
	return render_template("staff_manage_extraservice.html",data=data)
