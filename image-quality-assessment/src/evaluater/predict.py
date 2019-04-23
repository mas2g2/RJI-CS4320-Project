
import os
import glob
import json
import argparse
import mysql.connector
from utils.utils import calc_mean_score, save_json
from handlers.model_builder import Nima
from handlers.data_generator import TestDataGenerator

# TODO set up read_db_config
mydb = mysql.connector.connect(
  host="ec2-3-14-73-158.us-east-2.compute.amazonaws.com",
  user="adminUser",
  passwd="password123",
  database="rjiDB"
)
mycursor = mydb.cursor()

def image_file_to_json(img_path):
    img_dir = os.path.dirname(img_path)
    img_id = os.path.basename(img_path).split('.')[0]

    return img_dir, [{'image_id': img_id}]


def image_dir_to_json(img_dir, img_type='jpg'):
    img_paths = glob.glob(os.path.join(img_dir, '*.'+img_type))

    samples = []
    for img_path in img_paths:
        img_id = os.path.basename(img_path).split('.')[0]
        samples.append({'image_id': img_id})

    return samples


def predict(model, data_generator):
    return model.predict_generator(data_generator, workers=8, use_multiprocessing=True, verbose=1)


def main(base_model_name, weights_file, image_source, predictions_file, img_format='jpg'):
    print(weights_file)
    # load samples
    if os.path.isfile(image_source):
        image_dir, samples = image_file_to_json(image_source)
    else:
        image_dir = image_source
        samples = image_dir_to_json(image_dir, img_type='jpg')

    # build model and load weights
    nima = Nima(base_model_name, weights=None)
    nima.build()
    nima.nima_model.load_weights(weights_file)

    # initialize data generator
    data_generator = TestDataGenerator(samples, image_dir, 64, 10, nima.preprocessing_function(),
                                       img_format=img_format)

    # get predictions
    
    predictions = predict(nima.nima_model, data_generator)

    # calc mean scores and add to samples
    for i, sample in enumerate(samples):
        sample['mean_score_prediction'] = calc_mean_score(predictions[i])

    myJson = json.loads(json.dumps(samples, indent=2))
    #print(myJson)
    #print("hello")
    # TODO set up read_db_config
    

    for photo in myJson:
        print(photo['image_id'])
        sql = "UPDATE Photo SET aesthetic_rating = " + str(photo['mean_score_prediction']) + " WHERE filepath LIKE '%" + photo['image_id'] + "%'"
        #sql = "UPDATE Photo SET aesthetic_rating = 10"
        #sql = "insert into Photo(filepath,technical_rating,user_id) values ("+str(photo['image_id'])+","+str(photo['mean_score_prediction'])+",4)"
        #val = (photo['image_id'],photo['mean_score_prediction'])
        mycursor.execute(sql)
        mydb.commit()
        #print(sql)
        #print(photo['mean_score_prediction'])
    #with open('~/image-quality-assessment/predictions/predictions.json', 'w') as outfile:
        #json.dump(samples, outfile)
    #save_json(samples, '~/image-quality-assessment/predictions/predictions.json')
    #save_json(samples, '~/predictions/predictions.json')
    if predictions_file is not None:

        save_json(samples, predictions_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base-model-name', help='CNN base model name', required=True)
    parser.add_argument('-w', '--weights-file', help='path of weights file', required=True)
    parser.add_argument('-is', '--image-source', help='image directory or file', required=True)
    #parser.add_argument('-rt','--rating-type',help="type of rating",required=True)
    parser.add_argument('-pf', '--predictions-file', help='file with predictions', required=False, default=None)

    args = parser.parse_args()

    main(**args.__dict__)
