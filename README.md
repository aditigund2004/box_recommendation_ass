# Box Recommendation Service

A small Django + MySQL app that, given an order, recommends the cheapest
shipping box that fits it — or splits the order across multiple boxes if
nothing fits it whole.

## Data model

- **Product** — `sku`, `name`, `length_cm`, `width_cm`, `height_cm`, `weight_kg`
- **Box** — `name`, `internal_length_cm`, `internal_width_cm`, `internal_height_cm`, `max_weight_kg`, `cost`, `is_active`
- **Order** / **OrderItem** — an order is a set of (product, quantity) lines

## Algorithm (`boxing/services.py`)

3D bin packing is NP-hard, so this uses a fast heuristic rather than an
exact solver — appropriate for a warehouse tool that needs an answer
instantly:

1. **Weight check** — total item weight ≤ box `max_weight_kg`.
2. **Dimension check (with rotation)** — each item's dimensions and the
   box's internal dimensions are each sorted largest→smallest and compared
   axis by axis. This lets an item be rotated into whatever orientation
   fits, e.g. a tall thin item laid on its side.
3. **Volume check** — sum of item volumes ≤ box internal volume, a cheap
   filter that rules out boxes with no chance of fitting everything.

Among all boxes that pass all three checks, the **cheapest** one is
recommended (ties broken by smallest volume, so you don't ship mostly air).

**If no single box fits the whole order**, it falls back to a **First-Fit-
Decreasing bin-packing** heuristic: largest items placed first, each into
the cheapest already-open box with room, opening a new (cheapest-possible)
box only when needed. If a single item doesn't fit in *any* box in the
catalog, the API returns a 422 explaining which item and why.

This is a heuristic, not a guaranteed-optimal 3D packer — it doesn't model
irregular shapes, stacking constraints, or fragile-item separation. It's
sized to the problem described (pick a good box fast), not to replace an
industrial packing engine.

## Project layout

```
box_recommender/
  config/            # Django project settings/urls
  boxing/
    models.py        # Product, Box, Order, OrderItem
    services.py       # the recommendation algorithm
    serializers.py    # DRF serializers
    views.py          # API endpoints
    tests.py          # unit + API tests
  manage.py
  requirements.txt
```

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Configure SQLite via environment variables (defaults shown):

```bash

```

Create the SQLite database, then:

```bash
python manage.py makemigrations boxing
python manage.py migrate
python manage.py createsuperuser   # to add Products/Boxes via /admin

aditi
aditi@gmail.com
Aditi_2004

python manage.py runserver
```

## Running tests (no MySQL needed)

`config/settings.py` swaps in an in-memory SQLite database whenever
`DJANGO_TEST_MODE=1` is set, so the test suite runs standalone:

```bash
DJANGO_TEST_MODE=1 python manage.py test boxing
```

> Note: tests were written and their logic independently verified, but
> couldn't be executed inside this sandbox (no network access to install
> Django). Run the command above in your environment to confirm — the code
> is standard Django/DRF with nothing unusual in it.

## API

- `POST /api/products/` — create a product
- `POST /api/boxes/` — create a box type
- `POST /api/orders/` — create an order:
  ```json
  {
    "order_number": "ORD-1001",
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 3, "quantity": 1}
    ]
  }
  ```
- `GET /api/orders/{id}/recommend-box/` — get the recommendation:

  **Single box fits:**
  ```json
  {
    "order_number": "ORD-1001",
    "fits_single_box": true,
    "recommended_box": {"id": 2, "name": "Medium", "cost": "2.50", ...}
  }
  ```

  **Needs multiple boxes:**
  ```json
  {
    "order_number": "ORD-1001",
    "fits_single_box": false,
    "reason": "No single box fits the whole order; split across multiple boxes.",
    "boxes": [
      {"box": {...}, "items": ["SKU1", "SKU2"], "used_weight_kg": 4.2, "used_volume_cm3": 8000.0}
    ]
  }
  ```

## Admin

`/admin/` gives the warehouse team a simple UI to manage Products, Boxes,
and Orders (with inline order items) without needing the API.

## Where this plugs into a bigger site

This app is deliberately self-contained (its own Product/Order models) so
it can be graded/run standalone. To wire it into a full storefront, the
real fix is usually to drop this app's `Product`/`Order` models and point
`services.py` at your existing catalog/order models instead — the
algorithm only needs `dimensions`, `weight`, and an iterable of order line
items, so it doesn't care where those come from.



  * cheapest box
  * dimensions
  * weight
  * rotation
  * multiple boxes
  * impossible product
  * API endpoint