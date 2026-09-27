# V7 Performance Fix

The post-login Management load path was simplified.

- Management no longer requests the shared `/api/data/bootstrap` payload.
- Dashboard pages are code-split with React.lazy so unused HSE/employee/intelligence pages are not part of the initial bundle.
- The Management chunk begins preloading immediately after Management authentication.
- Notifications and health checks are deferred briefly so they do not compete with the first dashboard paint.
- A clear dashboard loading state is shown while the lazy page bundle is compiling/loading.
- Existing V6 features and backend APIs are preserved.
