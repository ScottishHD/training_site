import os
import babel
from sha_training_app import create_app

config_name = os.getenv('FLASK_CONFIG', 'development')
app = create_app(config_name)

@app.template_filter('datatime')
def format_datetime(value, fmt='medium'):
    if fmt == 'full':
        fmt = "EEEE, d. MMMM y 'at' HH:mm vvvv"
    elif fmt == 'medium':
        fmt = "dd/MM/y HH:mm"
    return babel.dates.format_datetime(value, fmt)

app.jinja_env.filters['datatime'] = format_datetime

if __name__ == '__main__':
    app.run()
