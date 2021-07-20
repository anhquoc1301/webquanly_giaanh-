from datetime import datetime
from nvr_api import downloadListPlates

# list_plates = getListPlates(datetime(year=2021, month=7, day=10))

downloadListPlates(datetime(year=2021, month=7, day=18))
# Print result
# for plate in list_plates:
#     print(plate)

# Save data as Excel document
# save_excel(list_plates,+)