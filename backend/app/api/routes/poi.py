"""Attraction photo API backed by Unsplash."""

from fastapi import APIRouter, HTTPException

from ...services.unsplash_service import get_unsplash_service

router = APIRouter(prefix="/poi", tags=["POI"])


@router.get(
    "/photo",
    summary="Get an attraction photo",
    description="Look up a representative photo for an attraction by name.",
)
async def get_attraction_photo(name: str):
    """Return a photo URL for the given attraction name."""
    try:
        unsplash_service = get_unsplash_service()

        photo_url = unsplash_service.get_photo_url(f"{name} China landmark")
        if not photo_url:
            photo_url = unsplash_service.get_photo_url(name)

        return {
            "success": True,
            "message": "ok",
            "data": {"name": name, "photo_url": photo_url},
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch photo for '{name}': {exc}",
        ) from exc