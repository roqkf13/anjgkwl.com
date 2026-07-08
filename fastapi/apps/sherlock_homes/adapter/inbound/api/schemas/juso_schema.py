from pydantic import BaseModel, Field

from sherlock_homes.app.dtos.juso_dto import ContactCommand


class JusoSchema(BaseModel):
    id: int = Field(0, description="Search ID")
    name: str = Field("주소 검색기", description="Service name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 14,
                "name": "주소 검색기 (Juso)",
            }
        }
    }


class ContactRowSchema(BaseModel):
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    phonetic_first_name: str = ""
    phonetic_middle_name: str = ""
    phonetic_last_name: str = ""
    name_prefix: str = ""
    name_suffix: str = ""
    nickname: str = ""
    file_as: str = ""
    organization_name: str = ""
    organization_title: str = ""
    organization_department: str = ""
    birthday: str = ""
    notes: str = ""
    photo: str = ""
    labels: str = ""
    e_mail_1_label: str = ""
    e_mail_1_value: str = ""
    e_mail_2_label: str = ""
    e_mail_2_value: str = ""
    phone_1_label: str = ""
    phone_1_value: str = ""

    def to_command(self) -> ContactCommand:
        return ContactCommand(**self.model_dump())


class ContactUploadResultSchema(BaseModel):
    total: int
    contacts: list[ContactRowSchema]


class ContactItemSchema(BaseModel):
    first_name: str = ""
    last_name: str = ""
    nickname: str = ""
    e_mail_1_value: str = ""
    e_mail_2_value: str = ""
    organization_name: str = ""


class ContactListSchema(BaseModel):
    total: int
    contacts: list[ContactItemSchema]
