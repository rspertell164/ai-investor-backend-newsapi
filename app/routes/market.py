from fastapi import APIRouter, Query, Body
from app.services import market_data

router = APIRouter(prefix="/api", tags=["Market Data"])

@router.get("/price")
async def price_lookup(symbol: str = Query(...)):
    return market_data.get_stock_price(symbol)

@router.get("/overview")
async def company_overview(symbol: str = Query(...)):
    return market_data.get_company_overview(symbol)

@router.get("/history")
async def historical_data(symbol: str = Query(...), interval: str = Query("daily")):
    return market_data.get_historical_data(symbol, interval)

@router.get("/news")
async def stock_news(symbol: str = Query(...)):
    return market_data.get_news(symbol)

@router.get("/technical")
async def technical_analysis(symbol: str = Query(...)):
    return market_data.get_technical_analysis(symbol)

@router.get("/fundamentals")
async def fundamentals(symbol: str = Query(...)):
    return market_data.get_fundamentals(symbol)

@router.get("/watchlist")
async def get_watchlist(user_id: str = Query(...)):
    return market_data.get_watchlist(user_id)

@router.post("/watchlist/add")
async def add_to_watchlist(user_id: str = Body(...), symbol: str = Body(...)):
    return market_data.add_to_watchlist(user_id, symbol)

@router.post("/watchlist/remove")
async def remove_from_watchlist(user_id: str = Body(...), symbol: str = Body(...)):
    return market_data.remove_from_watchlist(user_id, symbol)

@router.get("/alerts")
async def get_alerts(user_id: str = Query(...)):
    return market_data.get_alerts(user_id)

@router.post("/alerts/add")
async def add_alert(user_id: str = Body(...), symbol: str = Body(...), condition: str = Body(...)):
    return market_data.add_alert(user_id, symbol, condition)

@router.post("/alerts/remove")
async def remove_alert(user_id: str = Body(...), symbol: str = Body(...)):
    return market_data.remove_alert(user_id, symbol)
