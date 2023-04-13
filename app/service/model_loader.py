import glob
import joblib


class ModelLoader:
    def __get_latest_model_path(self) -> str:
        """Get latest model path"""
        try:
            return glob.glob("./model_store/sales_prediction*")[0]
        except Exception:
            FileNotFoundError("model does not exist")

    def get_latest_model(self) -> any:
        """Return model"""
        model_path = self.__get_latest_model_path()
        return joblib.load(model_path)
