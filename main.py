from data_load import DriveDataProvider, DrivingDataLoader, DriveDataSet, DataGenerator
from data_generators import center_image_generator, \
    center_left_right_image_generator, \
    left_image_generator, \
    right_image_generator, shift_image_generator, random_generators, pipe_line_generators
from trainer import Trainer

dataset = DriveDataSet("datasets/udacity-sample-track-1/driving_log.csv")

# data_generator = DataGenerator(center_left_right_image_generator)
# Trainer(learning_rate=0.0001, epoch=10).fit(data_generator.generate(dataset, batch_size=128))

data_generator = DataGenerator(pipe_line_generators(
    random_generators(center_image_generator, left_image_generator, right_image_generator),
    shift_image_generator
))
Trainer(learning_rate=0.0001, epoch=10).fit(data_generator.generate(dataset, batch_size=128))
