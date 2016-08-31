from flask import Flask, render_template
from peewee import *
from flask import request, redirect, url_for


app = Flask(__name__)
db = PostgresqlDatabase("user_story_db", user="adambodnar")
db.connect()

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db

class Story(BaseModel):
    story_title = CharField()
    user_story = TextField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = IntegerField
    status = IntegerField()

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

    for story in new_story:
        story = Story.create(story_title=request.form['story_title'],
                             user_story=request.form['user_story'],
                             acceptance_criteria=request.form['acceptance_criteria'],
                             business_value=request.form['business_value'],
                             estimation=float(request.form['estimation']),
                             status=request.form['status']
                             )
    return redirect(url_for('index'))


@app.route('/and/list', methods=['GET'])
def list_story():
    story = Story.query.all()
    return render_template('list.html', story=story)


Story.create_table()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
