# HiddenYatra — Performance Optimization Roadmap

This document outlines future performance enhancements for caching, image rendering, and network asset delivery.

---

## 1. Performance Optimization Tasks

1. **Redis Query Caching**:
   - Cache popular destination detail responses (`/place/<slug>`) and district lists (`/districts`) in Redis with automatic invalidation on admin edits.

2. **WebP Image Format Auto-Conversion**:
   - Implement automated server-side conversion of user-uploaded JPEGs/PNGs to WebP format for improved image compression and faster mobile page loads.

3. **CDN Integration**:
   - Serve static CSS/JS bundles and image uploads via Cloudflare or Amazon CloudFront CDN.

4. **HTTP/2 & HTTP/3 Server Push**:
   - Configure Nginx in production to enable HTTP/2 multiplexing for critical CSS and JS assets.
