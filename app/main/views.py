from flask import render_template,request,redirect,url_for,abort
from .import main
from ..models import Pitch,User
from .forms import UpdateProfile
from .. import db
from flask_login import login_required
import datetime



# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home-PITCHperfect'
    #review by category
    pitches_interview = Pitch.get_pitches('interview')
    pitches_product = Pitch.get_pitches('product')
    pitches_promotion = Pitch.get_pitches('promotion')


    return render_template('index.html',title = title, interview =pitches_interview , product = pitches_product, promotion = pitches_promotion)
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    count_pitches =Pitch.pitches_count(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,pitches =count_pitches,date = user_joined)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
  
