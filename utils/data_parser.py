"""Parsing and matching helpers for unnormalized listing data."""

import re
from typing import Literal, TypedDict


ALPHA_SIZE_RANKS = {
    "XXS": 1,
    "XS": 2,
    "S": 3,
    "M": 4,
    "L": 5,
    "XL": 6,
    "XXL": 7,
}


class AlphaSize(TypedDict):
    family: Literal["alpha"]
    min_rank: int
    max_rank: int


class WaistInseamSize(TypedDict):
    family: Literal["waist_inseam"]
    waist: int


class WaistInseamSizeWithInseam(WaistInseamSize):
    inseam: int


class ShoeSize(TypedDict):
    family: Literal["shoe_size"]
    system: Literal["US"]
    value: float


class OneSize(TypedDict):
    family: Literal["one_size"]


class UnknownSize(TypedDict):
    family: Literal["unknown"]
    raw: str


NormalizedSize = (
    AlphaSize
    | WaistInseamSize
    | WaistInseamSizeWithInseam
    | ShoeSize
    | OneSize
    | UnknownSize
)


def normalize_size(size: str) -> NormalizedSize:
    """Normalize one of the supported raw size systems.

    Inputs:
    size - size string, ex. W30 L30, M
    
    Recognized raw size strings:
    - alpha (``M``, ``S/M``, ``M/L``, ``XL (oversized)``)
    - measurements (``W30``, ``W30 L30``)
    - shoes (``US 7``, ``US 8.5``, ``US 9``)
    - free-size (``One Size``, ``One Size / Oversized``, ``One Size (adjustable)``)

    Returns:
    structured NormalizedSize dictionary, representing the size
    
    Alpha sizes support ``XXS`` through ``XXL`` and slash-separated combinations
    of those values.
    Parenthetical annotations are ignored.
    Other sizing systems are returned as unknown.
    """
    raw = size.strip().upper() # remove whitespace, convert to UPPERCASE

    # match ONE SIZE
    if re.match(r"^ONE SIZE", raw):
        return {"family": "one_size"}

    # strip parenthetical annotations + remove preceeding whitespace (replace with "")
    raw = re.sub(r"\s*\([^)]*\)", "", raw).strip()

   # match waist - ex. W30, L30
    waist_match = re.fullmatch(r"W(\d+)(?:\s*L(\d+))?", raw)
    if waist_match:
        result = {
                    "family": "waist_inseam",
          "waist": int(waist_match.group(1))  # W (waist) - required
        }
        if waist_match.group(2): # L (inseam) - optional
            result["inseam"] = int(waist_match.group(2))
        return result

    # match shoe size - ex. US 8
    shoe_match = re.fullmatch(r"US\s*(\d+(?:\.\d+)?)", raw)
    if shoe_match:
        return {
            "family": "shoe_size",
            "system": "US",
            "value": float(shoe_match.group(1)),
        }

    # match alpha values - ex. M, or S/M
    alpha_values = [part.strip() for part in raw.split("/")]
    if alpha_values and all(value in ALPHA_SIZE_RANKS for value in alpha_values):
        ranks = [ALPHA_SIZE_RANKS[value] for value in alpha_values]
        return {
            "family": "alpha",
            "min_rank": min(ranks),
            "max_rank": max(ranks),
        }

    # unknown system
    return {"family": "unknown", "raw": raw}


def size_matches(listing: dict, requested_size: str) -> bool:
    """Return whether a listing size satisfies a requested size.

    Inputs: 
    listing - item to check size match of
    requested_size - size to match

    Returns True if size matches
    
    Matching is category-blind and uses only normalized size systems:

    - Alpha sizes use ordered ranges. Ranges match when they overlap, so
      ``M`` matches ``S/M`` and ``M/L``.
    - Measurements use directional containment. Every requested field must be
      present with the same value in the listing, so ``W30`` matches ``W30 L30``
      but ``W30 L30`` does not match ``W30``.
    - US shoe sizes require the same US system and exact numeric value.
    - Free-size labels share one system; annotations such as ``oversized`` and
      ``adjustable`` are ignored.
    - Different, unsupported, and unknown systems never match.

    Examples:
        size_matches("M", "S/M") is True
        size_matches("W30", "W30 L30") is True
        size_matches("W30 L30", "W30") is False
        size_matches("US 9", "UK 9") is False
        size_matches("One Size", "One Size (adjustable)") is True
    """
    listing = normalize_size(listing["size"])        # dict holding normalized size
    requested = normalize_size(requested_size)

    if listing["family"] != requested["family"]:
        return False

    if listing["family"] == "alpha":
        return (
            listing["min_rank"] <= requested["max_rank"]        # check if overlap (match) exists
            and requested["min_rank"] <= listing["max_rank"]
        )

    if listing["family"] == "waist_inseam":         # if in request, check W/L property exists and value matches
        return all(                                 # in listing
            field in listing and listing[field] == value
            for field, value in requested.items()
            if field != "family"
        )

    if listing["family"] == "shoe_size":
      return listing["value"] == requested["value"]

    if listing["family"] == requested["family"] == "one_size":
      return True
    
    return False


def tokenize_text(text: str) -> list[str]:
    """
    Returns list containing tokenized keywords from text
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]+", " ", text)   # strip punctuation: replace non-word (character, number, _) and non-whitespace characters with empty string
    return text.split()

def listing_tokens(listing: dict) -> set[str]:
    """Return unique searchable tokens from the listing's text fields.

    Title and description are tokenized together. Style tags and colors are
    added directly in their original form.
    """
    tokens = set(tokenize_text(listing["description"]))
    tokens.update(tokenize_text(listing["title"]))
    
    tokens.update(listing["style_tags"])    # adds all elements from list to set
    tokens.update(listing["colors"])

    return tokens
