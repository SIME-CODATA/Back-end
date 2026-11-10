from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from Back_end.media_library.service.service import ( asset_file_path, get_asset, get_asset_by_name, grouped_public_assets, list_assets, normalize_folder, serialize_asset, )

router = APIRouter(prefix="/api/media", tags=["Media Library"])


@router.get("/public")
def public_media_library():
    return grouped_public_assets()


@router.get("/public/{folder}")
def public_media_folder(folder: str):
    try:
        folder = normalize_folder(folder)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"folder": folder, "items": [serialize_asset(a) for a in list_assets(folder=folder)]}


@router.get("/public/{folder}/{name}")
def public_media_by_name(folder: str, name: str):
    try:
        asset = get_asset_by_name(folder, name)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if asset is None:
        raise HTTPException(status_code=404, detail="Mídia não encontrada.")
    return serialize_asset(asset)


@router.get("/{asset_id}")
def media_metadata(asset_id: int):
    asset = get_asset(asset_id, include_inactive=True)
    if asset is None:
        raise HTTPException(status_code=404, detail="Mídia não encontrada.")
    payload = serialize_asset(asset)
    payload["is_active"] = asset.is_active
    return payload


@router.get("/{asset_id}/file")
def media_file(asset_id: int):
    asset = get_asset(asset_id, include_inactive=True)
    if asset is None:
        raise HTTPException(status_code=404, detail="Mídia não encontrada.")
    path = asset_file_path(asset)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Arquivo físico não encontrado.")
    return FileResponse(
        path=str(path),
        media_type=asset.mime_type,
        filename=asset.original_name,
        content_disposition_type="inline",
        headers={"Cache-Control": "public, max-age=3600" if asset.is_active else "no-store"},
    )
