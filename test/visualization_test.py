import unittest
import numpy.testing
import numpy as np
from data_load import FeedingData, record_allocation_random, record_allocation_angle_type
from data_load import DriveDataProvider, DrivingDataLoader, DriveDataSet, DataGenerator, \
    drive_record_filter_exclude_small_angles, drive_record_filter_include_all, drive_record_filter_exclude_zeros
from data_generators import image_itself, \
     shift_image_generator, random_generators, pipe_line_generators, pipe_line_random_generators, flip_generator
from visualization import Video, Plot
from performance_timer import Timer


class TestVideos(unittest.TestCase):
    def test_gif_for_generator(self):
        dataset = DriveDataSet("../datasets/udacity-sample-track-1/driving_log.csv")

        generator = pipe_line_generators(
            image_itself,
            shift_image_generator
        )
        Video.from_generators("resources/shift_center_images.gif", dataset[60], 0.0, 20, generator)

        # generator = pipe_line_generators(
        #     left_image_generator,
        #     shift_image_generator
        # )
        # Video.from_generators("resources/shift_left_images.gif", dataset[60], 0.2, 20, generator)
        #
        # generator = pipe_line_generators(
        #     right_image_generator,
        #     shift_image_generator
        # )
        # Video.from_generators("resources/shift_right_images.gif", dataset[60], -0.2, 20, generator)

    def test_create_sample_data_video(self):
        Video.from_udacity_sample_data(
            DriveDataSet("../datasets/udacity-sample-track-1/driving_log.csv", crop_images=False,
                         filter_method=drive_record_filter_include_all),
            "resources/sample_original.mp4")

    def test_create_sample_data_corp_video(self):
        Video.from_udacity_sample_data(
            DriveDataSet("../datasets/udacity-sample-track-1/driving_log.csv", crop_images=True,
                         filter_method=drive_record_filter_exclude_small_angles),
            "resources/sample_crop.mp4")


class TestPlot(unittest.TestCase):
    def create_real_dataset(self, filter_method):
        return DriveDataSet(
            "../datasets/udacity-sample-track-1/driving_log.csv",
            filter_method=filter_method
        )
    def test_angle_distribution(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_include_all)
        plt = Plot.angle_distribution(dataset.angles())
        plt.savefig("resources/angle_distribution.jpg")

    def test_angle_distribution_after_filterout_small_angles(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_exclude_small_angles)
        plt = Plot.angle_distribution(dataset.angles())
        plt.savefig("resources/angle_distribution_exclude_small_angles.jpg")

    def test_angle_distribution_after_filterout_zeros(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_exclude_zeros)
        plt = Plot.angle_distribution(dataset.angles())
        plt.savefig("resources/angle_distribution_exclude_zero_angles.jpg")

    def test_angle_distribution_generator(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_exclude_small_angles)
        generator = pipe_line_random_generators(
            image_itself,
            shift_image_generator(angle_offset_pre_pixel=0.003),
            flip_generator
        )
        data_generator = DataGenerator(generator)
        image, angles = next(data_generator.generate(dataset, 10000, record_allocation_method=record_allocation_random))
        plt = Plot.angle_distribution(angles)
        plt.savefig("resources/angle_distribution_generator.jpg")

    def test_angle_distribution_generator_exclude_small_angles(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_exclude_small_angles)
        generator = pipe_line_random_generators(
            image_itself,
            shift_image_generator(angle_offset_pre_pixel=0.003),
            flip_generator
        )
        data_generator = DataGenerator(generator)
        image, angles = next(data_generator.generate(dataset, 10000,
                                                     record_allocation_method=record_allocation_angle_type(40, 40)))
        plt = Plot.angle_distribution(angles)
        plt.savefig("resources/angle_distribution_generator_angle_40%_20%_40%.jpg")

    def test_angle_distribution_generator_exclude_small_angles_30_40_30(self):
        with Timer():
            dataset = self.create_real_dataset(filter_method=drive_record_filter_exclude_small_angles)
        generator = pipe_line_random_generators(
            image_itself,
            shift_image_generator(angle_offset_pre_pixel=0.002),
            flip_generator
        )
        data_generator = DataGenerator(generator)
        image, angles = next(data_generator.generate(dataset, 10000,
                                                     record_allocation_method=record_allocation_angle_type(30, 30)))
        plt = Plot.angle_distribution(angles)
        plt.savefig("resources/angle_distribution_generator_exclude_duplicated_small_angles_30_40_30.jpg")
