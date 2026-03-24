# ServiceLocator considered an anti-pattern but we need this to feel the pain and reasons to use DI frameworks later

from L3_Business_Logic.realty_service import RealtyService

RealtyService: RealtyService = RealtyService()
