# Static site image: nginx serving the repo content as-is.
# Multi-arch friendly (works on linux/amd64 and linux/arm64 for OCI Ampere).

FROM nginx:1.27-alpine

RUN apk add --no-cache brotli && \
    rm -rf /usr/share/nginx/html/* && \
    rm /etc/nginx/conf.d/default.conf

COPY deploy/nginx.conf /etc/nginx/nginx.conf

# Copy the full static site. The .dockerignore keeps junk out.
COPY . /usr/share/nginx/html

# Remove server-side-only files that should never be served.
RUN rm -rf \
      /usr/share/nginx/html/deploy \
      /usr/share/nginx/html/supabase \
      /usr/share/nginx/html/.github \
      /usr/share/nginx/html/server.js \
      /usr/share/nginx/html/package.json \
      /usr/share/nginx/html/package-lock.json \
      /usr/share/nginx/html/.env \
      /usr/share/nginx/html/.env.example \
      /usr/share/nginx/html/.gitignore \
      /usr/share/nginx/html/CLAUDE.md \
      /usr/share/nginx/html/node_modules

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1/healthz >/dev/null 2>&1 || exit 1

CMD ["nginx", "-g", "daemon off;"]
