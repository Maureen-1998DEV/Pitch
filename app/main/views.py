from flask import render_template,request,redirect,url_for,abort
from .import main
from ..models import Pitch,User,Comment
from .forms import UpdateProfile,PitchForm,CommentForm
from .. import db,photos
from flask_login import login_required,current_user
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

    return render_template('profile/update.html',form = form)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitch/new', methods = ['GET','POST'])
@login_required
def new_pitch():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        pitch = pitch_form.text.data
        category = pitch_form.category.data

        # Updated pitch 
        new_pitch = Pitch(title_pitch=title,content_pitch=pitch,category=category,user=current_user,likes=0,dislikes=0)

        # Save pitch 
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'New pitch'
    return render_template('newpitch.html',title = title,pitch_form=pitch_form )


@main.route('/pitches/pitches_promotion')
def pitches_promotion():

    pitches = Pitch.get_pitches('promotion')

    return render_template("promotion.html", pitches = pitches)


@main.route('/pitches/pitches_product')
def pitches_product():

    pitches = Pitch.get_pitches('product')

    return render_template("product.html", pitches = pitches)

@main.route('/pitches/pitches_interview')
def pitches_interview():

    pitches = Pitch.get_pitches('interview')

    return render_template("interview.html", pitches = pitches)

@main.route('/pitch/<int:id>', methods = ['GET','POST'])
def pitch(id):
    pitch = Pitch.get_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    elif request.args.get("dislike"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment= comment_form.text.data

        new_comment = Comment(content_commit = comment,user = current_user,pitch_id = pitch)

        new_comment.save_comment()


    comments = Comment.get_comment(pitch)

    return render_template("pitch.html", pitch = pitch, comment_form = comment_form, comments = comments, date = posted_date)

@main.route('/user/<uname>/pitches')
def user_pitches(uname):
    user = User.query.filter_by(username=uname).first()
    pitches = Pitch.query.filter_by(user_id = user.id).all()
    pitches_count = Pitch.count_pitches(uname)
    user_joined = user.date_joined.strftime('%b %d, %Y')

    return render_template("profile/pitches.html", user=user,pitches=pitches,pitches_count=pitches_count,date = user_joined)




