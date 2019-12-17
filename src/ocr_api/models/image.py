
class Image:

    def __init__(self, id, filename, date_uploaded, ocr_result_id=None):
        self.id = id
        self.filename = filename
        self.date_uploaded = date_uploaded
        self.ocr_result_id = ocr_result_id

    def __eq__(self, other):
        return all([
            self.filename == other.filename,
            self.date_uploaded == other.date_uploaded,
            self.ocr_result_id == other.ocr_result_id
        ])
