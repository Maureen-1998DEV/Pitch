from flask import render_template
from .import main
from ..models import Pitch





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


    
