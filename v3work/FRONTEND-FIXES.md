# OIL-SIF Frontend Accessibility & Usability Update

## Fixed
- Language switching now uses React state only. The previous DOM text-node mutation approach could translate already-translated text, causing stale language labels after switching languages.
- Language preference is persisted between sessions.
- RTL direction is applied for Urdu, Kashmiri and Sindhi selections.
- High Contrast is now a real high-contrast mode: black/white surfaces, strong borders, clearer focus states and stronger table contrast.
- Text accessibility now has three levels: normal, large and extra large.
- Report filters now query the full master dataset through `/api/data/reports` and actually change the returned records.
- Report search covers report ID, activity, precursor, Life-Saving Rule and report narrative.
- Review status, SIF status and activity filters are independent.
- Tables use readable labels, visible borders, alternating rows, sticky headers and horizontal scrolling instead of low-contrast text.

## Added for low-tech-flexibility users
- Quick Actions on Overview: Review Reports, View Risk Patterns and Ask Safety Assistant.
- Plain-language instructions before important actions.
- Quick examples for common field observations.
- Clearer screening result cards with required action separated from model output.
- Management drill-down now produces a practical recommendation based on selections.
- Help banner accessible from the top navigation.
- Better mobile navigation and responsive report controls.
- Stronger button, form and keyboard focus states.
- More explicit loading and empty states.

## Performance
The overview still loads from the compact overview endpoint. Report Analysis no longer waits for the old queue payload; it loads only the filtered records it needs from the master dataset.

## Backend addition
A small protected endpoint was added:
`GET /api/data/reports?search=&status=&review=&activity=&limit=`

The existing authentication, `/api/scan`, `/api/chat`, overview, intelligence and role dashboards remain compatible.
