import json
from google.api_core.client_options import ClientOptions
from google.cloud import automl
from google.cloud.automl_v1.proto import service_pb2

from flask import Flask, render_template, request
from forms import InputForm

file = "a.txt"
model =  "projects/930569794791/locations/us-central1/models/TCN4883944888674025472"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hackathon'

def inline_text_payload(file_path):
  with open(file_path, 'rb') as ff:
    content = ff.read()
  return {'text_snippet': {'content': content, 'mime_type': 'text/plain'} }

def pdf_payload(file_path):
  return {'document': {'input_config': {'gcs_source': {'input_uris': [file_path] } } } }

def get_prediction(file_path, model_name):
  options = ClientOptions(api_endpoint='automl.googleapis.com')
  prediction_client = automl.PredictionServiceClient(client_options=options)

  payload = inline_text_payload(file_path)

  params = {}
  request = prediction_client.predict(model_name, payload, params)
  return request  # waits until request is returned

@app.route('/', methods=['GET','POST'])
def inputForm():
    form = InputForm()
    if form.is_submitted():

        i = request.form.get("inputValue")

        with open('a.txt',"w") as f:
            f.write(str(i))
        mat = get_prediction(file,model)

        if float(mat.payload[0].classification.score) > float(mat.payload[1].classification.score):
            r = mat.payload[0].display_name

        elif mat.payload[0].classification.score < mat.payload[1].classification.score:
            r = mat.payload[1].display_name
        else:
            r = "Could not tell, proceed at your own risk!"
        #result = json.loads(dic)
        return render_template('form.html', form =form, result="The result we have found is " + r.lower())

    return render_template('form.html', form=form, result = "No result yet! Enter a description from a GoFundMe Description to find out if it is fake!")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
