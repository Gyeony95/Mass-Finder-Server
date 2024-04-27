from dataclasses import dataclass, field
from typing import Optional

from mass_finder_app.logic.enums import FormyType, IonType


@dataclass
class AminoModel:
    code: Optional[str] = None
    totalWeight: Optional[float] = None
    waterWeight: Optional[float] = None
    weight: Optional[float] = None
    formyType: Optional[FormyType] = None
    ionType: Optional[IonType] = None
    essentialSeq: Optional[str] = None
    similarity: Optional[float] = None

    @staticmethod
    def from_json(json_data):
        return AminoModel(
            code = json_data.get('code'),
            totalWeight = json_data.get('totalWeight'),
            waterWeight = json_data.get('waterWeight'),
            weight = json_data.get('weight'),
            formyType = FormyType.decode(json_data.get('formyType')),
            ionType = IonType.decode(json_data.get('ionType')),
            essentialSeq = json_data.get('essentialSeq'),
            similarity = json_data.get('similarity')
        )

    def to_json(self):
        return {
            'code': self.code,
            'totalWeight': self.totalWeight,
            'waterWeight': self.waterWeight,
            'weight': self.weight,
            'formyType': self.formyType.value if self.formyType else None,
            'ionType': self.ionType.text if self.ionType else None,
            'essentialSeq': self.essentialSeq,
            'similarity': self.similarity
        }
