# V5 Performance Fix

The Management dashboard previously built the full 2015-2025 geographic aggregation the first time the Management page was opened. The dataset is large enough that this could make the post-login transition feel slow.

This version includes a compact `backend/app_core/geography_cache.json` generated from the supplied January 2015-November 2025 dataset. The backend now reads this small cache first and only rebuilds from the CSV if the cache is missing or unreadable.

The geographic data, heatmap behavior, filters, timeline, state intelligence and other features are unchanged.
