from dataclasses import dataclass, field


@dataclass(frozen=True)
class JusoQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JusoResponse:
    id: int
    name: str


@dataclass(frozen=True)
class ContactCommand:
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


@dataclass
class ContactUploadResult:
    total: int
    contacts: list = field(default_factory=list)


@dataclass(frozen=True)
class ContactItem:
    first_name: str = ""
    last_name: str = ""
    nickname: str = ""
    e_mail_1_value: str = ""
    e_mail_2_value: str = ""
    organization_name: str = ""


@dataclass
class ContactListResult:
    total: int
    contacts: list = field(default_factory=list)
