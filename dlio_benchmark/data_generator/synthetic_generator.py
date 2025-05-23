"""
   Copyright (c) 2025, UChicago Argonne, LLC
   All Rights Reserved

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from dlio_benchmark.common.enumerations import Compression
from dlio_benchmark.data_generator.data_generator import DataGenerator

import logging
import numpy as np

from dlio_benchmark.utils.utility import progress, utcnow
from dlio_benchmark.utils.utility import Profile
from shutil import copyfile
import PIL.Image as im
from dlio_benchmark.common.constants import MODULE_DATA_GENERATOR

dlp = Profile(MODULE_DATA_GENERATOR)

class SyntheticGenerator(DataGenerator):
    def __init__(self):
        super().__init__()

    @dlp.log        
    def generate(self):
        """
        Generator for creating dummy files.
        """
        super().generate()
        np.random.seed(10)
        record_labels = [0] 
        dim = self.get_dimension(self.total_files_to_generate)
        for i in dlp.iter(range(self.my_rank, int(self.total_files_to_generate), self.comm_size)):
            out_path_spec = self.storage.get_uri(self._file_list[i])
            if self.my_rank == 0 and i % 100 == 0:
                self.logger.info(f"Generated file {i}/{self.total_files_to_generate}")
            progress(i+1, self.total_files_to_generate, "Generating Synethic Data (Empty)")
            prev_out_spec = out_path_spec
            with open(out_path_spec, 'w') as f:
                f.write(f"{i}")
        np.random.seed()