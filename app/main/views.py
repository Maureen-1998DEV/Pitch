from flask import render_template,request,redirect,url_for,abort
from .import main
from ..models import Pitch
from ..models import User




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

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

    
