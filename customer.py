from flask import*
from database import *

customer=Blueprint('customer',__name__)

@customer.route("/customerhome")
def customerhome():
	return render_template("customerhome.html")


@customer.route("/send_complaint",methods=['post','get'])
def send_complaint():
	data={}
	q="select * from complaint"
	res=select(q)
	data['view']=res
	if "submit" in request.form:
		complaint=request.form['complaint']
		q="insert into complaint values(null,'%s','%s','pending',curdate())"%(session['cus'],complaint)
		insert(q)
		return redirect(url_for("customer.send_complaint"))
	return render_template("customer_send_complaint.html",data=data)

@customer.route("/view_tables",methods=['post','get'])
def View_tables():
	data={}
	q="select * from tables where Table_status='pending'"
	res=select(q)
	data['view']=res
# q="select * from category where status='pending'"
# res=select(q)
# data['categoryview']=res
# return redirect(url_for("customer.send_complaint"))
	return render_template("customer_view_table.html",data=data)


@customer.route("/book_table",methods=['post','get'])
def book_table():
	data={}
	from datetime import date, datetime,timedelta
	today=date.today()
	
 
	import datetime

	# Get today's date and time
	now = datetime.datetime.now()

	# Get the time delta for one day
	one_day = datetime.timedelta(days=1)

	# Calculate the next day
	next_day = now + one_day
	print("###############################")
	print(next_day.strftime('%Y-%m-%d'))
	print("#######################")

	# Print the next day in YYYY-MM-DD format
	# print(next_day.strftime('%Y-%m-%d'))
	data['tomorrow']=next_day.strftime('%Y-%m-%d')




	q="SELECT *,booking.status as Status FROM `booking`,`customer`,`tables`,`category` WHERE `booking`.`Customer_id`=`customer`.`Customer_id` AND `booking`.`Table_id`=`tables`.`Table_id` AND `booking`.`Category_id`=`category`.`Category_id` AND  booking.Customer_id='%s' "%(session['cus'])
	res=select(q)
	data['viewbookings']=res
 
	if "action" in request.args:
		action=request.args['action']
			
		bid=request.args['bid']
	else:
		action=None

	if action=="cancel":
		q="update booking set Status='Cancelled' where Booking_id='%s'"%(bid)
		update(q)
		flash("Your booking has been cancelled")
		return redirect(url_for('customer.book_table'))

	# q="select * from menu"
	# res=select(q)
	# data['menu']=res
	q="select * from category where Status='1'"
	res=select(q)
	data['category']=res
 
	#q="select * from meal_time"
	#res=select(q)
	#data['meal_time']=res
 
	# q="select * from timeslot"
	# res1=select(q)
	# data['timeslot']=res1
 
	q="select * from tables"
	res2=select(q)
	data['tab']=res2
	# cid=request.args['cid']
	if "submit" in request.form:
		cat=request.form['cat']
		meal=request.form['meal']
		table=request.form['table']
		# menu=request.form['menu']
		date=request.form['date']
		q="select * from booking where Table_id='%s' and date='%s' and (status='paid' or status!='Cancelled')"%(table,date)
		print(q)
		res=select(q)
		print(res)
		q="select * from booking where Table_id='%s' and date='%s' and status='1' and Customer_id='%s'"%(table,date,session['cus'])
		r=select(q)

		if r:
			flash("You Already Booked this Table")
			return redirect(url_for('customer.book_table'))
		elif res:
			flash("Table Unavailable. Please select another table.")
			return redirect(url_for('customer.book_table'))
      
		else:
			s="select * from tables where Table_id='%s'"%(table)
			res3=select(s)
			q="insert into booking values(null,'%s','%s','%s','0','0','%s','0','%s','1')"%(session['cus'],cat,meal,table,date)	
			insert(q)
			q="update tables set Table_status='booked' where Table_id='%s'"%(res3[0]['Table_id'])
			update(q)
			flash("Table Reserved. Please select dishes from menu.")

			return redirect(url_for('customer.book_table'))
	return render_template("customer_book_table.html",data=data,date=today)


@customer.route('/customer_food_and_service',methods=['post','get'])
def customer_food_and_service():
    data={}
    q="SELECT * FROM  `menu`"
    data['menu']=select(q)
    
    q="SELECT * FROM  `extraservice`"
    data['service']=select(q)
    
    return render_template("customer_food_and_service.html",data=data)
    

@customer.route("/view_booked",methods=['post','get'])
def view_booked():
	data={}
	q="SELECT SUM(amount) as amount FROM `bookmenu` WHERE booking_id in (SELECT booking_id FROM `booking`WHERE customer_id='%s' AND booking.status='1')"%(session['cus'])
	res1=select(q)
	print(res1)
	if res1[0]['amount']!=None:
		amount=res1[0]['amount']
	else:
		amount=1 
	q1="SELECT SUM(price) as price FROM `extraservice_booked` INNER JOIN `extraservice` USING(`Extraservice_id`) WHERE booking_id in (SELECT booking_id FROM `booking`WHERE customer_id='%s' AND booking.status='1')"%(session['cus'])
	res2=select(q1)
	print(res2)
	if res2[0]['price']!=None:
		price=res2[0]['price']
	else:
		price=1
	total=int(amount)+int(price)
	data['total']=total 
	grantotal=int(total)+500
	data['grantotal']=grantotal

	
	q="SELECT * FROM `booking` INNER JOIN `bookmenu` USING (`Booking_id`) INNER JOIN `extraservice_booked` USING (`Booking_id`) INNER JOIN `menu` ON `bookmenu`.`Menu_id`=`menu`.`Menu_id` INNER JOIN `extraservice` USING (`Extraservice_id`) inner join tables using (Table_id) where customer_id='%s' and booking.status='1' group by Bookmenu_id"%(session['cus'])
	res=select(q)
	data['view']=res
 
	# q1="SELECT * FROM `booking` INNER JOIN `bookmenu` USING (`Booking_id`)  inner join tables using (Table_id) inner join meal_time using (meal_time_id) where booking.status='paid' group by Bookmenu_id"
	# pes=select(q1)
	# if pes:
	# 	data['s']="Not Available"
	
	
	
	return render_template("customer_view_booked.html",data=data)

@customer.route("/view_extraservice",methods=['post','get'])
def view_extraservice():
	data={}
	q="select * from extraservice inner join extraservice_booked INNER JOIN booking USING(Booking_id) "
	res=select(q)
	data['view']=res
	
	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
		bid=request.args['bid']
	else:
		action=None
	if action=="booking":
		q="insert into extraservice_booked values(null,'%s','%s')"%(cid,bid)
		insert(q)
		return redirect(url_for("customer.view_booked"))
	return render_template("customer_view_extraservice.html",data=data)


@customer.route("/view_extrabooked",methods=['post','get'])
def view_extrabooked():
	data={}
	q="select * from extraservice_booked inner join extraservice using(Extraservice_id) inner join booking using(booking_id) group by Extraservice_name"
	res=select(q)
	data['view']=res

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
		bid=request.args['bid']
	else:
		action=None

	if action=="remove":
		q="delete from extraservice_booked where extraservicebooked_id='%s'"%(cid)
		delete(q)
		return redirect(url_for('customer.view_extrabooked'))
	return render_template("customer_view_extrabooked.html",data=data)

@customer.route("/view_menu",methods=['post','get'])
def view_menu():
	data={}
	q="select * from menu inner join category using (category_id)"
	res=select(q)
	data['view']=res
	return render_template("customer_view_menu.html",data=data)

@customer.route("/add_food",methods=['post','get'])
def add_food():
	data={}


	q="select * from timeslot"
	res=select(q)
	data['timeslot']=res
	s="select * from tables where Table_status='pending'"
	res1=select(s)
	data['table']=res1
   

	mid=request.args['mid']
	menu=request.args['menu']
	data['up']=menu
	rate=request.args['rate']
	data['ups']=rate

	if "btn" in request.form:
		time=request.form['time']
		table=request.form['tables']
		qty=request.form['quantity']
		total=request.form['total']

		q="INSERT INTO `booking` VALUES(NULL,'%s','%s','%s','%s',CURDATE(),'booked')"%(session['cus'],time,table,total)
		print(q)
		oid=insert(q)
		q="INSERT INTO `bookmenu` VALUES(NULL,'%s','%s','%s','%s')"%(oid,mid,qty,rate)
		insert(q)

	return render_template("customer_add_food.html",data=data)

@customer.route("/view_foodbooked",methods=['post','get'])
def view_foodbooked():
	data={}
	q="SELECT * FROM menu inner join  bookmenu using(menu_id) INNER JOIN booking USING(Booking_id) INNER JOIN TABLES USING(Table_id) INNER JOIN timeslot USING(Timeslot_id)"
	res=select(q)
	data['view']=res
 
	
     

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
		bid=request.args['bid']
	else:
		action=None

		if action=="remove":
			q="delete from bookmenu where Bookmenu_id='%s'"%(cid)
			res=delete(q)
			q="update booking set Total=Total-'%s' where booking_id='%s'"%(res,bid)
			update(q)
			return redirect(url_for("customer.view_foodbooked"))
	return render_template("customer_view_foodbooked.html",data=data)

@customer.route('/customer_addcard',methods=['post','get'])
def customer_addcard():


	if "card" in request.form:

		
		num=request.form['num']
		name=request.form['name']

		d=request.form['date']

		q="select * from card where Customer_id='%s' and Card_no='%s'"%(session['cus'],num)
		res=select(q)
		if res:
			flash('Already Exist')

		else:


			from datetime import date,datetime

			d1=datetime.strptime(d,'%Y-%m')
			print(type(d1))


			today = datetime.today()
			print("Today's date:", type(today))

			print(d,")))))))))))")

			print(today)
			if d1 < today:
				flash('Card Expired. Please Add a Valid Card')
			else:
				q="insert into card values(null,'%s','%s','%s','%s') "%(session['cus'],num,name,d)
				insert(q)
				flash('Successfully added')
				return redirect(url_for('customer.view_booked'))
	return render_template('customer_addcard.html')

@customer.route("/payment",methods=['post','get'])
def payment():
	data={}
	q="SELECT * FROM menu inner join  bookmenu using(menu_id) INNER JOIN booking USING(Booking_id) where Customer_id='%s'"%(session['cus'])
	res=select(q)
	data['pay']=res
	q="select * from card where Customer_id='%s'"%(session['cus'])
	res1=select(q)
	data['carddrop']=res1
	cid=request.args['cid']
	bid=request.args['bid']
	rate=request.args['rate']
	

	if "submit" in request.form:
		card=request.form['card']
		q="insert into payment values(null,'%s','%s','%s',curdate())"%(card,cid,rate)
		insert(q)


		return redirect(url_for('customer.view_booked'))
		

	return render_template("customer_payment.html",data=data) 


@customer.route("/bookmenu",methods=['post','get'])
def bookmenu():
	data={}
	q="select * from  menu"

	res=select(q)
	data['menu']=res
	if "submit" in request.form:
		menu=request.form['menuid']
		q="select * from menu where Menu_id='%s'"%(menu)
		res=select(q)
		Rate=res[0]['Rate']
		qty=request.form['qty']
		bid=request.args['bid']
		pr=int(qty)*int(Rate)
		q="insert into bookmenu values(null,'%s','%s','%s','%s') "%(bid,menu,qty,pr)
		flash("Food Booked. Please book extra-service to continue.")
		insert(q)
		return redirect(url_for('customer.book_table'))
	return render_template('bookmenu.html',data=data)


@customer.route("/customer_services",methods=['post','get'])
def customer_services():
	data={}
	q="select * from  extraservice"

	res=select(q)
	
	data['services']=res
	if "submit" in request.form:
		services=request.form['servicesid']
		
		bid=request.args['bid']
		q="insert into extraservice_booked values(null,'%s','%s') "%(services,bid)
		insert(q)
		flash("Booked. Please go to bookings to continue")
		return redirect(url_for('customer.book_table'))
	return render_template('customer_services.html',data=data)


@customer.route("/makepayment",methods=['post','get'])
def makepayment():
	data={}
	q="select * from card where Customer_id='%s'"%(session['cus'])
	res=select(q)
	data['pay']=res

	bid=request.args['bid']
	
	total=request.args['total']
	grantotal=request.args['total']

	
	
	Price=total
	data['price']=Price
	print(data['price'])
	if "submit" in request.form:
		bid=request.args['bid']
		card=request.form['card']

		
		q="insert into payment values(null,'%s','%s','%s',curdate())"%(bid,card,Price)
		insert(q)
		flash("Payment Successful. Check Your Booking Details Below")
  
		q="update booking set status='paid' where booking_id='%s'"%(bid)
		update(q)
  
		return redirect(url_for('customer.book_table'))
	return render_template("makepayment.html",data=data) 

@customer.route('/viewbookednew')
def viewbookednew():
    data={}
    id=request.args['bid']
    q="SELECT * FROM `booking` INNER JOIN `bookmenu` USING (`Booking_id`) INNER JOIN `extraservice_booked` USING (`Booking_id`) INNER JOIN `menu` ON `bookmenu`.`Menu_id`=`menu`.`Menu_id` INNER JOIN `extraservice` USING (`Extraservice_id`) inner join tables using (Table_id) inner join category using (Category_id) where customer_id='%s' and booking.status='paid' and booking_id='%s' group by Bookmenu_id"%(session['cus'],id)
    res=select(q)
    data['view']=res
    return render_template('view_booked_new.html',data=data)


@customer.route('/viewbill')
def viewbill():
    data={}
    id=request.args['bid']
    q="SELECT * FROM `booking` INNER JOIN `bookmenu` USING (`Booking_id`) INNER JOIN `extraservice_booked` USING (`Booking_id`) INNER JOIN `menu` ON `bookmenu`.`Menu_id`=`menu`.`Menu_id` INNER JOIN `extraservice` USING (`Extraservice_id`) inner join tables using (Table_id) inner join category using (Category_id) where customer_id='%s' and booking.status='paid' and booking_id='%s' group by Bookmenu_id"%(session['cus'],id)
    res=select(q)
    data['view']=res
    # q="SELECT SUM(amount) as amount FROM `bookmenu` WHERE booking_id in (SELECT booking_id FROM `booking`WHERE customer_id='%s' AND booking.status='1')"%(session['cus'])
    # res1=select(q)
    # print(res1)
    # if res1[0]['amount']!=None:
    #     amount=res1[0]['amount']
    # else:
    #     amount=1 
    # q1="SELECT SUM(price) as price FROM `extraservice_booked` INNER JOIN `extraservice` USING(`Extraservice_id`) WHERE booking_id in (SELECT booking_id FROM `booking`WHERE customer_id='%s' AND booking.status='1')"%(session['cus'])
    # res2=select(q1)
    # print(res2)
    # if res2[0]['price']!=None:
    #     price=res2[0]['price']
    # else:
    #     price=1
    # total=int(amount)+int(price)
    # data['total']=total 
    # grantotal=int(total)+500
    # data['grantotal']=grantotal

    return render_template('view_bill.html',data=data)


