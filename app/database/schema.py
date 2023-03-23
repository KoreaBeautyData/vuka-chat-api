from pydantic import BaseModel

class DefaultReqModel(BaseModel):
    class Config:
        orm_mode = True

class DefaultResModel(BaseModel):
    class Config:
        orm_mode = True
    result: str = "Y"
    msg: str = None


class get_socialinfo_req(DefaultReqModel):
    social: str = None
    socialkey: str = None

class get_socialinfo_res(DefaultResModel):
    vkid: str = None

class get_socialinfo_all_req(DefaultReqModel):
    vkid: str = None

class get_socialinfo_all_res(DefaultResModel):
    kakao: str = None

class post_socialinfo_add_req(DefaultReqModel):
    vkid: str = None
    social: str = None
    socialkey: str = None
