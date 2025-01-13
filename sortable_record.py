class SortableRecord:
    def __init__(self, record):
        self.id = record.doc_id
        self.user_name = record['userName']
        self.sortable_timestamp, self.printable_timestamp = self.create_proper_timestamp(record)
        

    def create_proper_timestamp(self, record):
        sortable_timestamp = int(f"{record['year']:04}{record['month']:02}{record['day']:02}{record['hour']:02}{record['minute']:02}{record['second']:02}")
        printable_timestamp = f"{record['year']}-{record['month']:02}-{record['day']:02} {record['hour']:02}:{record['minute']:02}:{record['second']:02}"

        return sortable_timestamp, printable_timestamp
    
    def __str__(self):
        return f"ID: {self.id}, User Name: {self.user_name}, Timestamp: {self.printable_timestamp}"