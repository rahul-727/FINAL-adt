from flask import*
from database import *

public=Blueprint('public',__name__)

@public.route("/")
def home():
	return render_template("home.html")

@public.route('/login',methods=['post','get'])
def login():
	if "submit" in request.form:
		u=request.form['uname']
		p=request.form['pasd']
		q="select * from login where Username='%s' and Password='%s' and User_status=1"%(u,p)
		res=select(q)
		
		if res:
			# lid=res[0]['login_id']
			session['lid']=res[0]['Username']
			if res[0]['Usertype']=="admin":
				return redirect(url_for('admin.adminhome'))

			elif res[0]['Usertype']=="staff":
				q="select Staff_id from staff where Username='%s'"%(session['lid'])
				res2=select(q)
				if res2:
					session['sid']=res2[0]['Staff_id']
						
					return redirect(url_for('staff.staffhome'))

			elif res[0]['Usertype']=="customer":
				q="select *,concat(customer_fname,' ',customer_lname) as `c_name` from customer where Username='%s'"%(session['lid'])
				print(q)
				res3=select(q)
				if res3:

					session['cus']=res3[0]['Customer_id']
					session['c_name']=res3[0]['c_name']
					return redirect(url_for('customer.customerhome'))

			

	return render_template("login.html")



@public.route("/registration",methods=['post','get'])
def registration():
	if "submit" in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		phno=request.form['phn']
		email=request.form['email']
		uname=request.form['uname']
		pasd=request.form['pasd']
		q="select * from customer where Customer_email='%s'"%(email)
		ids=select(q)
		if ids:
			flash("Email Already Exists!")
		else:
			q="insert into login values('%s','%s','customer','1')"%(uname,pasd)
			insert(q)
			q="insert into customer values(null,'%s','%s','%s','%s','%s','1')"%(uname,fname,lname,phno,email)
			insert(q)
			flash('Successfuly Registered')
	return render_template("customer_registration.html")