from __future__ import annotations

import hashlib
import os
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

import reflex as rx
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from Back_end.media_library.models.model import MediaAsset


FOLDERS = ("imagens", "logos", "banners", "icons", "outros")
FOLDER_LABELS = {
    "imagens": "Imagens",
    "logos": "Logos",
    "banners": "Banners",
    "icons": "Ícones",
    "outros": "Outros",
}
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".mp4"}
MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".mp4": "video/mp4",
}
TYPE_BY_EXT = {
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".svg": "image",
    ".mp4": "video",
}
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,119}$")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def storage_root() -> Path:
    root = Path(os.getenv("MEDIA_STORAGE_PATH", "data/media")).resolve()
    root.mkdir(parents=True, exist_ok=True)
    for folder in FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)
    return root


def normalize_folder(folder: str) -> str:
    value = str(folder or "").strip().lower()
    if value not in FOLDERS:
        raise ValueError("Pasta inválida. Use imagens, logos, banners, icons ou outros.")
    return value


def validate_name(name: str) -> str:
    value = str(name or "").strip()
    if not value:
        raise ValueError("O nome/chave da mídia é obrigatório.")
    if not NAME_RE.fullmatch(value):
        raise ValueError(
            "Nome inválido. Use letras, números, ponto, hífen ou underline. "
            "Ex.: imagemHome, logoPrefeitura, bannerPrincipal."
        )
    return value


def _validate_svg(content: bytes) -> None:
    lower = content.lower()
    for token in (b"<!doctype", b"<!entity", b"<script", b"<foreignobject", b"javascript:", b"data:text/html"):
        if token in lower:
            raise ValueError("SVG recusado por conter conteúdo potencialmente inseguro.")
    try:
        root = ElementTree.fromstring(content)
    except ElementTree.ParseError as exc:
        raise ValueError("SVG inválido.") from exc
    if not (root.tag.lower() == "svg" or root.tag.lower().endswith("}svg")):
        raise ValueError("Arquivo SVG sem elemento raiz <svg>.")
    for element in root.iter():
        for attr, value in element.attrib.items():
            if str(attr).lower().startswith("on"):
                raise ValueError("SVG recusado por conter eventos JavaScript.")
            if str(attr).lower().endswith("href"):
                href = str(value).strip().lower()
                if href.startswith(("javascript:", "http://", "https://", "//")):
                    raise ValueError("SVG recusado por conter referência externa.")


def detect_media(original_name: str, content: bytes) -> tuple[str, str, str]:
    ext = Path(original_name or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Formato não suportado. Imagens: PNG, JPEG/JPG, SVG. Vídeo: MP4.")
    if not content:
        raise ValueError("O arquivo enviado está vazio.")

    valid = False
    if ext == ".png":
        valid = content.startswith(b"\\x89PNG\\r\\n\\x1a\\n")
    elif ext in {".jpg", ".jpeg"}:
        valid = len(content) >= 3 and content[:3] == b"\\xff\\xd8\\xff"
    elif ext == ".mp4":
        valid = len(content) >= 12 and content[4:8] == b"ftyp"
    elif ext == ".svg":
        _validate_svg(content)
        valid = True

    if not valid:
        raise ValueError("O conteúdo do arquivo não corresponde ao formato informado.")

    return TYPE_BY_EXT[ext], MIME_BY_EXT[ext], ext


def _max_bytes(media_type: str) -> int:
    env = "MEDIA_MAX_VIDEO_MB" if media_type == "video" else "MEDIA_MAX_IMAGE_MB"
    default = "500" if media_type == "video" else "25"
    return int(os.getenv(env, default)) * 1024 * 1024


def get_asset(asset_id: int, *, include_inactive: bool = False) -> MediaAsset | None:
    with rx.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None or (not include_inactive and not asset.is_active):
            return None
        session.expunge(asset)
        return asset


def get_asset_by_name(folder: str, name: str) -> MediaAsset | None:
    folder = normalize_folder(folder)
    name = validate_name(name)
    with rx.session() as session:
        asset = session.exec(
            select(MediaAsset).where(
                MediaAsset.folder == folder,
                MediaAsset.name == name,
                MediaAsset.is_active == True,  # noqa: E712
            )
        ).first()
        if asset:
            session.expunge(asset)
        return asset


def list_assets(*, search: str = "", media_type: str = "all", folder: str = "all") -> list[MediaAsset]:
    with rx.session() as session:
        query = select(MediaAsset).where(MediaAsset.is_active == True)  # noqa: E712
        if media_type in {"image", "video"}:
            query = query.where(MediaAsset.media_type == media_type)
        if folder in FOLDERS:
            query = query.where(MediaAsset.folder == folder)
        rows = list(session.exec(query.order_by(MediaAsset.folder, MediaAsset.name)).all())
        for row in rows:
            session.expunge(row)

    term = str(search or "").strip().casefold()
    if not term:
        return rows
    return [
        a for a in rows
        if term in str(a.name).casefold()
        or term in str(a.original_name).casefold()
        or term in str(a.alt_text).casefold()
        or term in str(a.description).casefold()
    ]


def save_asset(*, original_name: str, content: bytes, name: str, folder: str,
               alt_text: str = "", description: str = "", actor_user_id: int | None = None) -> MediaAsset:
    name = validate_name(name)
    folder = normalize_folder(folder)
    media_type, mime_type, extension = detect_media(original_name, content)

    if len(content) > _max_bytes(media_type):
        limit = os.getenv("MEDIA_MAX_VIDEO_MB" if media_type == "video" else "MEDIA_MAX_IMAGE_MB",
                          "500" if media_type == "video" else "25")
        raise ValueError(f"Arquivo acima do limite de {limit} MB.")

    checksum = hashlib.sha256(content).hexdigest()
    storage_name = f"{uuid.uuid4().hex}{extension}"
    relative_path = f"{folder}/{storage_name}"
    destination = storage_root() / relative_path
    now = _utc_now()

    with rx.session() as session:
        duplicate = session.exec(
            select(MediaAsset).where(
                MediaAsset.folder == folder,
                MediaAsset.name == name,
                MediaAsset.is_active == True,  # noqa: E712
            )
        ).first()
        if duplicate:
            raise ValueError(f'Já existe uma mídia chamada "{name}" na pasta "{folder}".')

        destination.write_bytes(content)
        try:
            asset = MediaAsset(
                name=name,
                folder=folder,
                original_name=original_name,
                storage_name=storage_name,
                relative_path=relative_path,
                media_type=media_type,
                mime_type=mime_type,
                extension=extension,
                size_bytes=len(content),
                checksum_sha256=checksum,
                alt_text=alt_text.strip(),
                description=description.strip(),
                is_active=True,
                created_by=actor_user_id,
                updated_by=actor_user_id,
                created_at=now,
                updated_at=now,
            )

            session.add(asset)
            session.commit()
            session.refresh(asset)
            session.expunge(asset)

            return asset

        except Exception:
            session.rollback()

            if destination.exists():
                destination.unlink()

            raise


def update_asset(*, asset_id: int, name: str, folder: str, alt_text: str = "",
                 description: str = "", actor_user_id: int | None = None) -> MediaAsset:
    name = validate_name(name)
    folder = normalize_folder(folder)

    with rx.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None or not asset.is_active:
            raise ValueError("Arquivo não encontrado.")

        duplicate = session.exec(
            select(MediaAsset).where(
                MediaAsset.folder == folder,
                MediaAsset.name == name,
                MediaAsset.id != asset_id,
                MediaAsset.is_active == True,  # noqa: E712
            )
        ).first()
        if duplicate:
            raise ValueError(f'Já existe uma mídia chamada "{name}" na pasta "{folder}".')

        if asset.folder != folder:
            old_path = asset_file_path(asset)
            new_relative = f"{folder}/{asset.storage_name}"
            new_path = storage_root() / new_relative
            if old_path.exists():
                shutil.move(str(old_path), str(new_path))
            asset.relative_path = new_relative

        asset.name = name
        asset.folder = folder
        asset.alt_text = str(alt_text or "").strip()
        asset.description = str(description or "").strip()
        asset.updated_by = actor_user_id
        asset.updated_at = _utc_now()
        session.add(asset)
        session.commit()
        session.refresh(asset)
        session.expunge(asset)
        return asset


def archive_asset(*, asset_id: int, actor_user_id: int | None = None) -> MediaAsset:
    with rx.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None or not asset.is_active:
            raise ValueError("Arquivo não encontrado.")
        asset.is_active = False
        asset.updated_by = actor_user_id
        asset.updated_at = _utc_now()
        session.add(asset)
        session.commit()
        session.refresh(asset)
        session.expunge(asset)
        return asset


def asset_file_path(asset: MediaAsset) -> Path:
    return storage_root() / str(asset.relative_path or asset.storage_name).lstrip("/")


def public_prefix() -> str:
    prefix = os.getenv("MEDIA_PUBLIC_PREFIX", "/backend").strip()
    return "" if not prefix else "/" + prefix.strip("/")


def public_asset_url(asset_id: int,) -> str:
    prefix = str(
        os.getenv(
            "MEDIA_PUBLIC_PREFIX",
            "/backend",
        )
        or ""
    ).strip()

    path = f"/api/media/{asset_id}/file"

    # URL absoluta, ambiente local por exemplo:
    # http://localhost:8000
    if prefix.startswith(
        ("http://", "https://")
    ):
        return (
            f"{prefix.rstrip('/')}"
            f"{path}"
        )

    # Prefixo relativo de produção:
    # /backend
    if prefix:
        normalized = (
            "/"
            + prefix.strip("/")
        )

        return (
            f"{normalized}"
            f"{path}"
        )

    return path


def serialize_asset(asset: MediaAsset) -> dict:
    return {
        "id": int(asset.id or 0),
        "name": asset.name,
        "folder": asset.folder,
        "media_type": asset.media_type,
        "mime_type": asset.mime_type,
        "extension": asset.extension,
        "original_name": asset.original_name,
        "size_bytes": asset.size_bytes,
        "alt_text": asset.alt_text,
        "description": asset.description,
        "url": public_asset_url(int(asset.id or 0)),
        "api_path": f"/api/media/{asset.id}/file",
        "updated_at": asset.updated_at.isoformat() if asset.updated_at else None,
    }


def grouped_public_assets() -> dict[str, list[dict]]:
    result = {folder: [] for folder in FOLDERS}
    for asset in list_assets():
        result[asset.folder].append(serialize_asset(asset))
    return result
