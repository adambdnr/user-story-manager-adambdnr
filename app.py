from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adambodnar:123@localhost/user_stories'
db = SQLAlchemy(app)
db.create_all()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_title = db.Column(db.String(80), unique=True)
    user_story = db.Column(db.Text)
    acceptance_criteria = db.Column(db.Text)
    business_value = db.Column(db.Integer)
    estimation = db.Column(db.Integer)
    status = db.Column(db.String(30))

    def __init__(self,
                 story_title,
                 user_story,
                 acceptance_criteria,
                 business_value,
                 estimation,
                 status
                 ):

        self.story_title = story_title
        self.user_story = user_story
        self.acceptance_criteria = acceptance_criteria
        self.business_value = business_value
        self.estimation = estimation
        self.status = status

    # def __repr__(self):
    #    return '<Story %r>' % self.story_title


@app.route('/')
def index():
    return render_template('form.html')


# @app.route('/story/<story_id>', methods=['GET'])
# def get_one_story(story_id):
#    story = Story.query.filter_by(story_id=story.id).first()
#    return redirect(url_for('index'))


@app.route('/story', methods=['POST'])
def story_post():
    new_story = Story(request.form['story_title'],
                      request.form['user_story'],
                      request.form['acceptance_criteria'],
                      request.form['business_value'],
                      float(request.form['estimation']),
                      request.form['status']
                      )

    db.session.add(new_story)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/and/list', methods=['GET'])
def list_story():
    story = Story.query.all()
    return render_template('list.html', story=story)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
