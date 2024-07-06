IMAGES_PATH = './images'
DATABASE_NAME = 'images.db'


from flask import Flask, jsonify, request, send_file;
from ImageService import ImageService
from flask_sqlalchemy import SQLAlchemy
from DatabaseService import ImageDatabaseService;
import os

app = Flask(__name__);
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DATABASE_NAME)
db = SQLAlchemy(app)

imageDatabaseService = ImageDatabaseService(db);
imageService = ImageService();

with app.app_context():
    db.create_all();



def writeFile(path, data):
    
    #store image file with url added to image path
    filePath = '{}/{}'.format(IMAGES_PATH, path);
    os.makedirs(os.path.dirname(str(filePath)), exist_ok=True)
    with open(filePath, 'wb') as f:
        f.write(data)
    return filePath
    
    
@app.route('/download_images' , methods=['POST'])
def download_images():
    urls = request.json.get('urls', None)
    if urls == None or len(urls) == 0:
        return 'No urls provided'
    output = []
    for url in urls:
        if imageDatabaseService.readById(url) != None:
            print('Image with url {} already exists'.format(url))
            output.append('Image with url {} already exists'.format(url))
            continue
        image = imageService.download_image(url)
        if image == None:
            print('Image not found')
            output.append('Image with url {} not found'.format(url))
            # skip to the next iteration
            continue
        
        filePath = writeFile(url, image)
        
        imageDatabaseService.write(url , filePath)
        output.append('Image with url {} downloaded'.format(url))
        
    # send 202 status code
    return jsonify(output), 202;

# create endpoints for getting list of image and retrieving an image by providing a url.
@app.route('/list_images', methods=['GET'])
def get_images():
    result = imageDatabaseService.readAll();
    # transform the result to a list of urls
    urls = []
    for image in result:
        urls.append(image.url)
    return jsonify(urls);

@app.route('/get_image', methods=['GET'])
def get_image():
    url = request.args.get('url', None)
    if url == None or url == '':
        return 'Image url not provided', 400
    image = imageDatabaseService.readById(url)
    if image == None:
        return 'Image not found', 404
    
    return send_file(image.path, mimetype='image/jpg')

    
@app.errorhandler(404)
def page_not_found(e):
    return 'Endpoint not found', 404;

if __name__ == '__main__':
    app.run(debug=True, port=5000);
    
