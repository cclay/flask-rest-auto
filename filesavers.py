__author__ = 'cscharfe'


def save_photoupload(request, car_id):
    photo_savepath = _save_photoupload(request, car_id)
    return photo_savepath[1:]  #remove the .

def _save_photoupload(request, car_id):
    photo_savepath = "not set"
    if request.files.has_key('photoupload'):
        photo_file = request.files['photoupload']
        unique_filename = _get_clean_filename(photo_file.filename, car_id)
        photo_savepath = "./static/images/" + unique_filename
        _save_file(photo_file, photo_savepath)
    return photo_savepath


def _get_clean_filename(filename, car_id):
    name = filename.replace("../", "").replace("./", "")
    return str(car_id) + "_" + name


def _save_file(fil, path):
    data = fil.read()
    try:
        path = path.encode('ascii', 'ignore')
        f = open(path, "wb")
        f.write(data)
        f.close()
        return path
    except IOError as e:
        print e
        return ""
