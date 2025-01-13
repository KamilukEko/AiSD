from db_manager import DatabaseManager
from radix_sort import radix_sort
from sortable_record import SortableRecord

db = DatabaseManager()
db_data = db.get_all()

sortable_array = []
for record in db_data:
    sortable_array.append(SortableRecord(record))

radix_sort(sortable_array)

for record in sortable_array:
    print(record)

