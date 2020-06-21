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
        result = request.form
        i = request.form.get("inputValue")

        with open('a.txt',"w") as f:
            f.write(str(i))
        print(get_prediction(file,model))
        return render_template('output.html', result=result)

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
