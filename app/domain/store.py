from pydantic import BaseModel, validator


class StoreInput(BaseModel):
    Store: int
    DayOfWeek: int
    Date: str
    Customers: int
    Open: int
    Promo: int
    StateHoliday: str
    SchoolHoliday: int

    @validator('DayOfWeek')
    def must_be_between_one_or_seven(cls, v):
        if v >= 7 and v <= 0:
            raise ValueError(f'must be between 1 or 7')
        return v
    
    @validator('Open')
    def open_is_one_or_zero(cls, v):
        if v != 1 or v != 0:
            raise ValueError(f'must be either 1 or 0')
        return v
    
    @validator('Promo')
    def promo_is_one_or_zero(cls, v):
        if v != 1 or v != 0:
            raise ValueError(f'must be either 1 or 0')
        return v
    
    @validator('StateHoliday')
    def must_belong_to_state_holiday_category(cls, v):
        categories = {'0', 'a', 'b', 'c'}
        if v not in categories:
            raise ValueError(
                f'must belong to the following categories: {categories}'
            )
        return v
        
    @validator('SchoolHoliday')
    def school_holiday_is_one_or_zero(cls, v):
        if v != 1 or v != 0:
            raise ValueError(f'must be either 1 or 0')
        return v
