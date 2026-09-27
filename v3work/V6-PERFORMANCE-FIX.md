# V6 Performance Fix

The V6 package keeps the V5 UI/features and fixes a major frontend performance bottleneck.

## Main fix
The multilingual runtime previously installed a `MutationObserver` even when the interface was in English. Every React DOM update could trigger a full-document text scan (`TreeWalker`). The Management Command Center has many DOM nodes and interactive updates, so this could make the post-login render feel very slow.

V6 now:
- skips the MutationObserver entirely for English;
- keeps the observer for non-English languages;
- slightly debounces non-English translation work;
- removes React StrictMode in the Vite development entry point to avoid duplicate effect execution during local development;
- caches Management site/geography requests in the frontend;
- prevents the Management geographic request from being tied to the unrelated reporting-period control.

The backend geographic cache remains in place.
