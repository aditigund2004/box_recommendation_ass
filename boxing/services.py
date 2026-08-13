"""
Box recommendation logic.

The problem is a variant of 3D bin packing (NP-hard in general), so this
implements a fast, explainable HEURISTIC rather than an exact solver —
appropriate for a warehouse tool that needs an answer in milliseconds, not
a perfect mathematical optimum.

Two checks decide whether an item (or the whole order) can go in a box:

1. Weight check   — total item weight <= box.max_weight_kg
2. Dimension check — each item, independently, must fit inside the box when
   both the item's dimensions and the box's internal dimensions are sorted
   largest-to-smallest and compared axis-by-axis. This correctly allows for
   rotating the item into whichever orientation fits (e.g. laying a tall
   item on its side), which a naive length/width/height compare would miss.
3. Volume check   — sum of item volumes <= box internal volume, as a cheap
   necessary (not sufficient) condition that filters out boxes with no hope
   of fitting everything, without running a full 3D packing simulation.

Single-box recommendation: among all boxes that pass all three checks for
the *entire* order, pick the cheapest one (ties broken by smallest volume,
so we don't over-ship air).

Multi-box fallback: if no single box fits the whole order, items are split
across multiple boxes using a First-Fit-Decreasing bin-packing heuristic —
largest items placed first, into the cheapest already-open box that has
room, opening a new box only when needed.
"""
from dataclasses import dataclass, field
from typing import List, Optional

from .models import Box, Order


@dataclass
class PackedUnit:
    """One physical unit to be packed (a Product exploded out by quantity)."""

    sku: str
    dimensions: tuple
    weight: float

    @property
    def volume(self):
        l, w, h = self.dimensions
        return l * w * h


@dataclass
class BinResult:
    box: Box
    units: List[PackedUnit] = field(default_factory=list)

    @property
    def used_weight(self):
        return sum(u.weight for u in self.units)

    @property
    def used_volume(self):
        return sum(u.volume for u in self.units)


@dataclass
class RecommendationResult:
    fits_single_box: bool
    box: Optional[Box] = None
    bins: Optional[List[BinResult]] = None  # populated only when fits_single_box is False
    reason: str = ""


def _fits_rotated(item_dims, container_dims) -> bool:
    """True if item_dims fits inside container_dims in *some* orientation."""
    item_sorted = sorted(item_dims, reverse=True)
    container_sorted = sorted(container_dims, reverse=True)
    return all(i <= c for i, c in zip(item_sorted, container_sorted))


def _explode_order_to_units(order: Order) -> List[PackedUnit]:
    units = []
    for item in order.items.select_related("product").all():
        for _ in range(item.quantity):
            units.append(
                PackedUnit(
                    sku=item.product.sku,
                    dimensions=item.product.dimensions,
                    weight=float(item.product.weight_kg),
                )
            )
    return units


def _candidate_boxes():
    return list(Box.objects.filter(is_active=True))


def box_fits_order(box: Box, units: List[PackedUnit]) -> bool:
    """All three checks (weight / per-item dimension / total volume) for one box."""
    total_weight = sum(u.weight for u in units)
    if total_weight > float(box.max_weight_kg):
        return False

    total_volume = sum(u.volume for u in units)
    if total_volume > float(box.volume_cm3):
        return False

    for u in units:
        if not _fits_rotated(u.dimensions, box.dimensions):
            return False

    return True


def recommend_single_box(units: List[PackedUnit], boxes: List[Box]) -> Optional[Box]:
    candidates = [b for b in boxes if box_fits_order(b, units)]
    if not candidates:
        return None
    return min(candidates, key=lambda b: (b.cost, b.volume_cm3))


def recommend_multi_box(units: List[PackedUnit], boxes: List[Box]) -> List[BinResult]:
    """First-Fit-Decreasing: largest units first, cheapest box that has room."""
    if not boxes:
        return []

    # Only consider boxes that can hold at least this single unit on its own —
    # otherwise no box in the catalog can ever ship it.
    sorted_units = sorted(units, key=lambda u: u.volume, reverse=True)
    boxes_by_cost = sorted(boxes, key=lambda b: (b.cost, b.volume_cm3))

    open_bins: List[BinResult] = []

    for unit in sorted_units:
        placed = False
        # Try existing open bins first (cheapest already-open bin with room).
        for bin_ in open_bins:
            projected = bin_.units + [unit]
            if box_fits_order(bin_.box, projected):
                bin_.units.append(unit)
                placed = True
                break

        if placed:
            continue

        # Open a new bin: cheapest box type that can hold this unit alone.
        for box in boxes_by_cost:
            if box_fits_order(box, [unit]):
                open_bins.append(BinResult(box=box, units=[unit]))
                placed = True
                break

        if not placed:
            # No box in the whole catalog can hold this single item.
            raise ValueError(
                f"No available box can fit item '{unit.sku}' "
                f"({unit.dimensions[0]}x{unit.dimensions[1]}x{unit.dimensions[2]} cm, "
                f"{unit.weight} kg) even on its own."
            )

    return open_bins


def recommend_box_for_order(order: Order) -> RecommendationResult:
    units = _explode_order_to_units(order)
    if not units:
        return RecommendationResult(fits_single_box=False, reason="Order has no items.")

    boxes = _candidate_boxes()
    if not boxes:
        return RecommendationResult(fits_single_box=False, reason="No active box types configured.")

    best = recommend_single_box(units, boxes)
    if best is not None:
        return RecommendationResult(fits_single_box=True, box=best)

    bins = recommend_multi_box(units, boxes)
    return RecommendationResult(
        fits_single_box=False,
        bins=bins,
        reason="No single box fits the whole order; split across multiple boxes.",
    )
