
class OcrResult:

    def __init__(id, image_id, ocr_conversion_status, text,
                 word_confidence_levels, date_converted):
        self.id = id
        self.image_id = image_id
        self.ocr_conversion_status = ocr_conversion_status
        self.text = text
        self.word_confidence_levels = word_confidence_levels
        self.date_converted = date_converted
