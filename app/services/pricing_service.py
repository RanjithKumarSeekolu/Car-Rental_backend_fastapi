import math

from app.core.config import settings

CATALOG_HOST_ID = "SEED_USER_ADMIN"


def js_round(value: float) -> int:
    """Round like JavaScript's Math.round (0.5 always rounds up)."""
    return math.floor(value + 0.5)


def is_catalog_listing(car: dict) -> bool:
    return car.get("isPlatformListing") is True or car.get("hostId") == CATALOG_HOST_ID


def split_fare(total_price, is_catalog: bool) -> dict:
    total = js_round(float(total_price or 0))
    if is_catalog:
        return {"isCatalog": True, "platformFeeRate": 1, "platformFee": total, "hostPayout": 0}

    rate = settings.platform_fee_rate
    platform_fee = js_round(total * rate)
    return {
        "isCatalog": False,
        "platformFeeRate": rate,
        "platformFee": platform_fee,
        "hostPayout": total - platform_fee,
    }


def resolve_split(booking: dict) -> dict:
    if booking.get("platformFee") is not None and booking.get("hostPayout") is not None:
        is_catalog = bool(booking.get("isCatalog"))
        default_rate = 1 if is_catalog else settings.platform_fee_rate
        return {
            "isCatalog": is_catalog,
            "platformFeeRate": booking.get("platformFeeRate") or default_rate,
            "platformFee": booking.get("platformFee") or 0,
            "hostPayout": booking.get("hostPayout") or 0,
        }

    is_catalog = booking.get("isCatalog") is True or booking.get("hostId") == CATALOG_HOST_ID
    return split_fare(booking.get("totalPrice"), is_catalog)