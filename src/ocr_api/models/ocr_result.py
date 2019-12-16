
class OcrResult:

    def __init__(self, id, image_id, ocr_conversion_status, text,
                 date_converted):
        self.id = id
        self.image_id = image_id
        self.ocr_conversion_status = ocr_conversion_status
        self.text = text
        self.date_converted = date_converted
