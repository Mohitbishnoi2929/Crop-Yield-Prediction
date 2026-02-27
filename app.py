from flask import Flask, render_template
from page.Predictive_page import predict_bp

app = Flask(__name__)

# Register blueprint
app.register_blueprint(predict_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
