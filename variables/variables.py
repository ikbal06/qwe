from datetime import datetime

from RPA.Robocorp.utils import get_output_dir


# Current date formatted as a string in YYYY-MM-DD format.
TODAY = datetime.strftime(datetime.now(), "%Y-%m-%d")

# File which gets attached in the output Work Items produced by the Producer. This file
#  is generated by a pre-run script configured in the robot.yaml during rcc/cloud runs.
WORKITEM_FILE_PATH = str(get_output_dir() / "random-workitem-file.txt")
