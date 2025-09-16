# from pydantic import BaseModel, field_validator
# from datetime import datetime
# from typing import Optional, Union

# class ExternalCurriculumData(BaseModel):
#     ID: int
#     ID_OKSO: Optional[int] = None
#     ID_PLAN_TYPE: int
#     ID_DISC_CYCLE: Optional[int] = None
#     ID_TRAINING_FORMS: int
#     ID_STUDY_PERIOD: int
#     BASE_CREDITS: Optional[float] = None
#     VAR_CREDITS: Optional[float] = None
#     ID_CURR_CONSTRS: Optional[int] = None
#     ID_INDEP_WORK_NORMS: Optional[int] = None
#     TOTAL_CREDITS: Optional[float] = None
#     IS_BACH_REQ: bool = False
#     IS_SHORT: bool = False
#     ID_STAGE_REQ: Optional[int] = None
#     YEAR_ENROL: int
#     ID_PARENT_CURRICULUM: Optional[int] = None
#     COPY_NUMBER: int = 0
#     VERSION_NUMBER: int = 0
#     ID_COPY_REASON: Optional[int] = None
#     ID_DEVELOPER: int
#     ID_RESPONSIBLE: int
#     C2H: int
#     C2H_MIN: int
#     C2H_MAX: int
#     LAST_MODIFIED: str
#     CREATED: Optional[str] = None
#     REMARK: Optional[str] = None
#     HAS_GE: bool = False
#     ID_STATUS: int
#     IS_BY_CYCLES_BAD: bool = False  # Делаем значение по умолчанию
#     CREDITS: float
#     PUBLISH_DATE: str
#     FSK_FACULTET: Optional[Union[str, int]] = None  # Принимаем и string и int
#     ID_DEAN: Optional[int] = None
#     ID_CHAIR_HEAD: Optional[int] = None
#     ID_OKSO_MODULE: Optional[int] = None
#     ID_OKSO_PROFILE: Optional[int] = None
#     SEM_START_PROFILE: Optional[int] = None
#     ID_CHAIR: Optional[int] = None
#     TYPE_BAC: Optional[int] = None  # Делаем Optional
#     ID_LEVEL: Optional[int] = None
#     DURATION_MONTHS: int
#     FK_PROJECT_ORGANIZATION: Optional[int] = None
#     ID_CURRICULUM_PROTOCOL: Optional[int] = None
#     ID_WP_RESP: Optional[int] = None
#     PAGES: Optional[int] = None
#     ID_FGOS: Optional[int] = None
#     FK_FOREIGN_LANGS: int = 0
#     IS_TRACKS: bool = False
#     EDIT_CM_DEVELOPERS: bool = False
#     ID_PDF_DOC: Optional[int] = None
#     ID_FILE_G: Optional[int] = None
    
#     # Валидаторы для обработки особых случаев
#     @field_validator('IS_BY_CYCLES_BAD', 'HAS_GE', 'IS_BACH_REQ', 'IS_SHORT', 'IS_TRACKS', 'EDIT_CM_DEVELOPERS', mode='before')
#     @classmethod
#     def handle_null_bool(cls, v):
#         """Обрабатывает None для boolean полей"""
#         if v is None:
#             return False
#         return bool(v)
    
#     @field_validator('FSK_FACULTET', mode='before')
#     @classmethod
#     def handle_fsk_facultet(cls, v):
#         """Конвертирует FSK_FACULTET в string"""
#         if v is None:
#             return None
#         return str(v)  # Конвертируем число в строку
    
#     @field_validator('TYPE_BAC', 'ID_STAGE_REQ', 'ID_DISC_CYCLE', mode='before')
#     @classmethod
#     def handle_null_int(cls, v):
#         """Обрабатывает None для integer полей"""
#         if v is None:
#             return None
#         return int(v)
    
#     def to_internal(self) -> CurriculumCreate:
#         return CurriculumCreate(
#             id_okso=self.ID_OKSO,
#             id_plan_type=self.ID_PLAN_TYPE,
#             id_disc_cycle=self.ID_DISC_CYCLE,
#             id_training_forms=self.ID_TRAINING_FORMS,
#             id_study_period=self.ID_STUDY_PERIOD,
#             base_credits=self.BASE_CREDITS,
#             var_credits=self.VAR_CREDITS,
#             id_curr_constrs=self.ID_CURR_CONSTRS,
#             id_indep_work_norms=self.ID_INDEP_WORK_NORMS,
#             total_credits=self.TOTAL_CREDITS,
#             is_bach_req=self.IS_BACH_REQ,
#             is_short=self.IS_SHORT,
#             id_stage_req=self.ID_STAGE_REQ,
#             year_enrol=self.YEAR_ENROL,
#             id_parent_curriculum=self.ID_PARENT_CURRICULUM,
#             copy_number=self.COPY_NUMBER,
#             version_number=self.VERSION_NUMBER,
#             id_copy_reason=self.ID_COPY_REASON,
#             id_developer=self.ID_DEVELOPER,
#             id_responsible=self.ID_RESPONSIBLE,
#             c2h=self.C2H,
#             c2h_min=self.C2H_MIN,
#             c2h_max=self.C2H_MAX,
#             last_modified=datetime.fromisoformat(self.LAST_MODIFIED.replace('Z', '+00:00')),
#             created=datetime.fromisoformat(self.CREATED.replace('Z', '+00:00')) if self.CREATED else None,
#             remark=self.REMARK,
#             has_ge=self.HAS_GE,
#             id_status=self.ID_STATUS,
#             is_by_cycles_bad=self.IS_BY_CYCLES_BAD,
#             credits=self.CREDITS,
#             publish_date=datetime.fromisoformat(self.PUBLISH_DATE.replace('Z', '+00:00')),
#             fsk_facultet=str(self.FSK_FACULTET) if self.FSK_FACULTET is not None else None,
#             id_dean=self.ID_DEAN,
#             id_chair_head=self.ID_CHAIR_HEAD,
#             id_okso_module=self.ID_OKSO_MODULE,
#             id_okso_profile=self.ID_OKSO_PROFILE,
#             sem_start_profile=self.SEM_START_PROFILE,
#             id_chair=self.ID_CHAIR,
#             type_bac=self.TYPE_BAC,
#             id_level=self.ID_LEVEL,
#             duration_months=self.DURATION_MONTHS,
#             fk_project_organization=self.FK_PROJECT_ORGANIZATION,
#             id_curriculum_protocol=self.ID_CURRICULUM_PROTOCOL,
#             id_wp_resp=self.ID_WP_RESP,
#             pages=self.PAGES,
#             id_fgos=self.ID_FGOS,
#             fk_foreign_langs=self.FK_FOREIGN_LANGS,
#             is_tracks=self.IS_TRACKS,
#             edit_cm_developers=self.EDIT_CM_DEVELOPERS,
#             id_pdf_doc=self.ID_PDF_DOC,
#             id_file_g=self.ID_FILE_G
#         )