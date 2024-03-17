from pydantic import BaseModel

class TranscriptFeedbackCreate(BaseModel):
    TranscriptSegmentId: int  # Ensure the field name matches the model
    Description: str
    isCorrect: int
class TranscriptFeedback(BaseModel):
    Id: int
    TranscriptSegmentId: int
    Description: str
    isCorrect: int
