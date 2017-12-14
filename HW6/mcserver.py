import ConfigParser, logging, datetime, os, json

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("search-form.html")


@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    now = datetime.datetime.now()
    startdate = request.form['startdate'].split("/")
    enddate = request.form['enddate'].split("/")
    sdate = datetime.date( int(startdate[0]), int(startdate[1]), int(startdate[2]))
    edate =  datetime.date(int(enddate[0]),int(enddate[1]), int(enddate[2]))
    results = mc.sentenceCount(keywords,
                               solr_filter=[mc.publish_date_query(sdate , edate),
                                            'tags_id_media:9139487'], split=True, split_start_date = "-".join(startdate), split_end_date="-".join(enddate))
    data = []
    # print(results['split'])
    for i in results['split']:
        temp_dict = {}
        temp_dict['name'] = keywords
        temp_dict['x'] = i
        temp_dict['y'] = results['split'][i]
        data.append(temp_dict)
    # print(data)

    return render_template("search-results.html",
                           keywords=keywords,
                           sentenceCount=results['count'],
                           plotdata = json.dumps(data, sort_keys=True) )

if __name__ == "__main__":
    app.debug = True
    app.run()
