#  #!/usr/bin/env python
#   Copyright (c) 2019. ShiJie Sun at the Chang'an University
#   This work is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License.
#   For a copy, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.
#   Author: shijie Sun
#   Email: shijieSun@chd.edu.cn
#   Github: www.github.com/shijieS
#
#
from dataset.amot.amot_reader import AmotTestDataset
import numpy as np
from config import config
from layers.dmmn.tracker import Tracker, Config
import os




if __name__ == "__main__":
    dataset = AmotTestDataset()
    tracker = Tracker("Amot", "V1", config)

    index = 0
    sequence_name = None
    while index < len(dataset):
        # 1. if switch video, then save and clear all tracks
        current_sequence_name = dataset.sequence_list[dataset.get_groupd_index(index)]
        if sequence_name is None:
            sequence_name = current_sequence_name
            Config.set_image_folder(
                os.path.join(config['test']['image_save_folder'], ''.join(current_sequence_name.replace('/', '-')[-5:])[:-4])
            )

        if sequence_name not in current_sequence_name:
            save_mot_folder = os.path.join(config["test"]["log_save_folder"], "mot")
            if not os.path.exists(save_mot_folder):
                os.makedirs(save_mot_folder)
            mot_file = os.path.join(save_mot_folder,
                                    "{}.txt".format(''.join(sequence_name.split('/')[-5:])[:-4]))
            tracker.save_mot_result(mot_file, True)
            Config.set_image_folder(
                os.path.join(config['test']['image_save_folder'], ''.join(current_sequence_name.replace('/', '-')[-5:])[:-4])
            )

        sequence_name = current_sequence_name

        # 2. get items
        frames, times, start_frame_index = dataset[index]

        # 3. update trackers
        result_frames = tracker.update(frames, times, start_frame_index)

        # 4. save mot results
        save_mot_folder = os.path.join(config["test"]["log_save_folder"], "mot")
        if not os.path.exists(save_mot_folder):
            os.makedirs(save_mot_folder)
        mot_file = os.path.join(save_mot_folder,
                                "{}.txt".format(''.join(sequence_name.split('/')[-5:])[:-4]))
        tracker.save_mot_result(mot_file)

        index += (dataset.max_frame_num_with_scale - Config.share_frame_num)
