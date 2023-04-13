from fastapi import APIRouter

from app.domain.store import StoreSchema
from app.service.preprocessor import StorePreprocessor
from app.service.model_loader import ModelLoader

router = APIRouter(tags=['inference'])

processor = StorePreprocessor()
loader = ModelLoader()
model = loader.get_latest_model()


@router.post('/predict')
async def predict(store: StoreSchema) -> dict[str, float]:
    x = await processor.convert(store)
    sales = model.predict(x)[0]
    return {"sales": sales}
